import json
from django.test import TestCase
from django.test import Client
from graphene.test import Client as GrapheneClient
import inflection


from django.test import RequestFactory, TestCase


# Inherit from this in your test cases
class GraphQLTestCase(TestCase):

    def setUp(self):
        self._client = Client()
        self.token = None

        from PersonalDataApi.schema import schema
        self._gqlclient = GrapheneClient(schema)

        from django.contrib.auth.models import User
        self.user = User.objects.get(username="guest")

        from MetaDataApi.users.models import Profile

    def execute_test_client_api_query(
            self, api_query, user=None, variable_values=None, **kwargs):
        """
        Returns the results of executing a graphQL query using the graphene
        test client.  This is a helper method for our tests
        """
        request_factory = RequestFactory()
        context_value = request_factory.get('/api/')
        context_value.user = user
        client = self._gqlclient
        executed = client.execute(
            api_query, context_value=context_value,
            variable_values=variable_values, **kwargs)
        return executed

    def execute(self, query: str, operation_name: str = None,
                variables: dict = None):

        body = {'query': query}
        if operation_name:
            body['operation_name'] = operation_name
        if variables:
            body['variables'] = variables

        header = {"Authorization": "JWT " + self.token} if self.token else {}

        executed = self._gqlclient.execute(
            json.dumps(body), context_value=header)

        return executed

    def query(self, query: str, operation_name: str = None,
              variables: dict = None):
        '''
        Args:
            query (string) - GraphQL query to run
            op_name (string) - If the query is a mutation or named query, you
            must supply the op_name.  For annon queries ("{ ... }"),
            should be None (default).
            input (dict) - If provided, the $input variable in GraphQL will be
            set to this value

        Returns:
            dict, response from graphql endpoint.  The response has the "data"
             key. It will have the "error" key if any error happened.
        '''
        body = {'query': query}
        if operation_name:
            body['operation_name'] = operation_name
        if input:
            body['variables'] = variables

        header = {"Authorization": "JWT " + self.token} if self.token else {}

        resp = self._client.post('/graphql', json.dumps(body),
                                 content_type='application/json',
                                 **header)
        jresp = json.loads(resp.content.decode())
        return jresp

    def login(self, username: str = "guest", password: str = "test1234"):
        # User.objects.create(username='test', password='hunter2')
        resp = self.execute(
            # The mutation's graphql code
            '''
            mutation LoginMutation($username: String!, $password: String!) {
                tokenAuth(username: $username, password: $password) {
                  token
                }
            }
            ''',
            # The operation name (from the 1st line of the mutation)
            operation_name='LoginMutation',
            variables={'username': username, 'password': password}
        )
        self.assertResponseNoErrors(resp)
        self.token = resp["data"]["tokenAuth"]["token"]
        self._client.defaults['Authorization'] = "JWT " + self.token

    def assertResponseNoErrors(self, resp: dict, expected: dict = None):
        '''
        Assert that the resp (as retuened from query) has the data from
        expected
        '''
        self.assertNotIn('errors', resp, 'Response had errors')
        if expected is not None:
            self.assertEqual(resp['data'], expected,
                             'Response has correct data')

    def response_to_datapoints(self, resp, mutationname):

        datapointlist = []

        resplist = resp["data"][mutationname]

        for key, value in resplist.items():

            if key == "datapoint":
                datapointlist.append(self.dict_to_datapoint(value))
        return datapointlist

    def dict_to_datapoint(self, dict):
        from PersonalDataApi.datapoints.models import Datapoint, CategoryTypes
        us_dict = {}
        # convert all keys to underscore
        for key, value in dict.items():
            us_dict[inflection.underscore(key)] = dict[key]

        return Datapoint(
            # id=obj["id"],
            datetime=us_dict["datetime"],
            category=CategoryTypes.force_value(us_dict["category"]),
            source_device=us_dict["source_device"],
            value=us_dict["value"],
            text_from_audio=us_dict["text_from_audio"]
        )

    def response_to_user_and_profile(self, resp):
        pass

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import unittest

import django

from tests.GraphQLTestCase import GraphQLTestCase


# TODO: Configure your database in settings.py and sync before running tests.


class DatapointTestCase(GraphQLTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(DatapointTestCase, cls).setUpClass()
        django.setup()

    @unittest.skip("needs repair")
    def test_login_mutation_successful(self):
        # User.objects.create(username='test', password='hunter2')

        resp = self.query(
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
            variables={'username': 'guest', 'password': 'test1234'}
        )
        self.assertResponseNoErrors(resp)

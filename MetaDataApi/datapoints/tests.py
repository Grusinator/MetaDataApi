"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
import django
#from django.contrib.auth import get_user_model


from MetaDataApi.tests.GraphQLTestCase import GraphQLTestCase

# TODO: Configure your database in settings.py and sync before running tests.
Token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiZXhwIjoxNTM1MTE4NTA1LCJvcmlnX2lhdCI6MTUzNTExODIwNX0.Behbkb_R3OPuPubuoO0TIVl9jr-oPNgDTFBLvassKmU'


class DatapointTestCase(GraphQLTestCase):
    """Tests for the application views."""
    # Django requires an explicit setup() when running tests in PTVS

    @classmethod
    def setUpClass(cls):
        django.setup()

    def test_create_test_datapoint(self):
        input = {
            "datetime": '2018-08-27T09:41:17.912790+00:00',
            "category": "test",
            "source_device": "insomnia",
            "value": 2.0,
            "text_from_audio": "test"
        }

        resp = self.execute_test_client_api_query(
            # The mutation's graphql code
            '''
            mutation createDatapointMutation(
	            $datetime: DateTime, 
	            $category: CategoryTypes,
	            $source_device: String!,
	            $value: Float,
	            $text_from_audio: String
            ) {
              createDatapoint(
		            datetime:$datetime, 
		            category:$category,
		            sourceDevice:$source_device,
		            value:$value,
		            textFromAudio:$text_from_audio
	            )
                {
                datapoint{
                    datetime
	                category
	                sourceDevice
	                value
	                textFromAudio
                }
                }
            }
            ''',
            variable_values=input,
            user=self.user
        )

        datapoint = self.response_to_datapoints(resp, "createDatapoint")[0]

        inputdatapoint = self.dict_to_datapoint(input)

        test = datapoint == inputdatapoint
        self.assertEqual(datapoint, inputdatapoint)

        self.assertResponseNoErrors(resp)

    def test_create_datapoint_audiodata(self):
        # User.objects.create(username='test', password='hunter2')

        self.login()

        input = {
            "datetime": None,
            "category": "speech_audio",
            "source_device": "insomnia",
            "value": None,
            "text_from_audio": None
        }

        output = {
            "datetime": None,
            "category": "speech_audio",
            "sourceDevice": "insomnia",
            "value": None,
            "textFromAudio": None
        }

        resp = self.execute(
            # The mutation's graphql code
            '''
            mutation createDatapointMutation(
	            $datetime: DateTime, 
	            $category: CategoryTypes,
	            $source_device: String!,
	            $value: Float,
	            $text_from_audio: String
            ) {
              createDatapoint(
		            datetime:$datetime, 
		            category:$category,
		            sourceDevice:$source_device,
		            value:$value,
		            textFromAudio:$text_from_audio
	            )
                {
                    datetime
	                category
	                sourceDevice
	                value
	                textFromAudio
                }
            }
            ''',
            # The operation name (from the 1st line of the mutation)
            operation_name='createDatapointMutation',
            variables=input
        )

        self.assertResponseNoErrors(resp, {"createDatapoint": output})

# from datetime import datetime

# import boto3
# import django
# from django.core.files import File
# from django.test import TransactionTestCase
# from moto import mock_s3

# from MetaDataApi.metadata.tests import LoadTestData

# MY_BUCKET = "my_bucket"
# MY_PREFIX = "mock_folder"


# @mock_s3
# class test_RdfsDataProviders(TransactionTestCase):
#     @classmethod
#     def setUpClass(cls):
#         django.setup()
#         super(test_RdfsDataProviders, cls).setUpClass()

#     def setUp(self):
#         self.client = boto3.client(
#             "s3",
#             region_name="eu-west-1",
#             aws_access_key_id="fake_access_key",
#             aws_secret_access_key="fake_secret_key",
#         )
#         # try:
#         #     s3 = boto3.resource(
#         #         "s3",
#         #         region_name="eu-west-1",
#         #         aws_access_key_id="fake_access_key",
#         #         aws_secret_access_key="fake_secret_key",
#         #     )
#         #     s3.meta.client.head_bucket(Bucket=MY_BUCKET)
#         # except ClientError:
#         #     pass
#         # else:
#         #     err = "{bucket} should not exist.".format(bucket=MY_BUCKET)
#         #     raise EnvironmentError(err)
#         # client.create_bucket(Bucket=MY_BUCKET)
#         # current_dir = os.path.dirname(__file__)
#         # fixtures_dir = os.path.join(current_dir, "fixtures")
#         # _upload_fixtures(MY_BUCKET, fixtures_dir)

#     def tearDown(self):
#         s3 = boto3.resource(
#             "s3",
#             region_name="eu-west-1",
#             aws_access_key_id="fake_access_key",
#             aws_secret_access_key="fake_secret_key",
#         )
#         bucket = s3.Bucket(MY_BUCKET)
#         for key in bucket.objects.all():
#             key.delete()
#         bucket.delete()


#     def test_create_dataprovider(self):
#         from MetaDataApi.metadata.rdfs_models.meta_data_api.rdfs_data_provider import RdfsDataProvider

#         LoadTestData.init_meta_data_api()
#         RdfsDataProvider.create_data_provider()

#     def test_create_datadump(self):
#         LoadTestData.init_meta_data_api()

#         file = File("test mocked data file")

#         from MetaDataApi.metadata.rdfs_models.meta_data_api.rdfs_data_provider import RdfsDataProvider
#         self.client.create_bucket(Bucket=MY_BUCKET)
#         provider = RdfsDataProvider.create_data_provider()
#         RdfsDataProvider.create_data_dump(
#             provider, datetime(1, 1, 1, 1, 1, 1), file)

#         from MetaDataApi.metadata.models import FileAttributeInstance
#         file_att = FileAttributeInstance.objects.all().first()
#         self.assertEqual(file, file_att.value)

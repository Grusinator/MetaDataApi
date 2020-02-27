# Create your tests here.
import unittest
from unittest.mock import patch

import django
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model
from model_bakery import baker

from MetaDataApi.utils import JsonUtils
from MetaDataApi.utils.django_utils import django_file_utils
from MetaDataApi.utils.unittest_utils.unittest_utils import get_method_path
from dataproviders import tasks
from dataproviders.models import DataFetch, Endpoint, DataFileUpload
from dataproviders.models.DataFile import DataFile
from dataproviders.services.transform_files_to_data import TransformFilesToData
from dataproviders.tests.mock_objects.mock_data_fetch import data_fetch_json_strava_activity
from dynamic_models import tasks as dynamic_model_tasks

TAGS = set("slow")


class TestRunTasks(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()

    def tearDown(self) -> None:
        super().tearDown()
        # ModelDefinition.objects.all().delete()

    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE} ")
    def test_clean_data_from_data_fetch(self):
        with patch(get_method_path(DataFetch.execute_on_save_methods)) as mock_method:
            data, data_fetch, user = self.create_data_fetch_objects()
            self.assertIsNone(DataFile.objects.first())
            tasks.clean_data_from_source(data_fetch.pk, is_from_file_upload=False)
            self.assertIsNotNone(DataFile.objects.first())

    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    def test_clean_data_from_data_file_upload(self):
        with patch(get_method_path(DataFileUpload.execute_on_save_methods)) as mock_method:
            data, data_file_upload, user = self.create_data_file_upload_objects()
            self.assertIsNone(DataFile.objects.first())
            tasks.clean_data_from_source(data_file_upload.pk, is_from_file_upload=True)
            self.assertIsNotNone(DataFile.objects.first())

    @unittest.skip("cant get activity, but only when running all")
    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    def test_build_data_from_data_fetch(self):
        with patch(get_method_path(DataFetch.execute_on_save_methods)) as mock_method:
            data, data_fetch, user = self.create_data_fetch_objects()
            TransformFilesToData().create_data_file(data, user, data_fetch)
            dynamic_model_tasks.build_models_from_data_files(pk=data_fetch.refined_data_file.pk)
            model = get_dynamic_model("activity")
            self.assertIsNotNone(model)

    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    def test_build_data_from_data_file_upload(self):
        with patch(get_method_path(DataFileUpload.execute_on_save_methods)) as mock_method:
            data, data_file_upload, user = self.create_data_file_upload_objects()
            TransformFilesToData().create_data_file(data, user, data_file_upload)
            dynamic_model_tasks.build_models_from_data_files(pk=data_file_upload.refined_data_file.pk)
            model = get_dynamic_model("activity")
            self.assertIsNotNone(model)

    def create_data_fetch_objects(self):
        user = baker.make(User.__name__)
        data_file = self.build_test_data_file()
        data = data_fetch_json_strava_activity()
        endpoint = baker.make(Endpoint.__name__, endpoint_name="activity")
        data_fetch = baker.make(DataFetch.__name__, make_m2m=True, data_file_from_source=data_file,
                                endpoint=endpoint, )
        return data, data_fetch, user

    def create_data_file_upload_objects(self):
        user = baker.make(User.__name__)
        data_file = self.build_test_data_file()
        data_file_upload = baker.make(DataFileUpload.__name__, make_m2m=True, data_file_from_source=data_file)
        data = data_fetch_json_strava_activity()
        return data, data_file_upload, user

    def build_test_data_file(self):
        data = data_fetch_json_strava_activity()
        data_str = JsonUtils.dumps(data)
        return django_file_utils.convert_str_to_file(data_str, filetype=django_file_utils.FileType.JSON)

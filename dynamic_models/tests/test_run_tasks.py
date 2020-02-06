# Create your tests here.
import unittest
from unittest.mock import patch, Mock

import django
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model

from MetaDataApi.utils import JsonUtils
from MetaDataApi.utils.django_model_utils import django_file_utils
from dataproviders.models import DataFetch, DataProviderUser, DataProvider, Endpoint, DataFileUpload
from dataproviders.models.DataFile import DataFile
from dataproviders.services import InitializeDataProviders, transform_files_to_data
from dataproviders.tests.mock_objects.mock_data_fetch import data_fetch_json_strava_activity
from dynamic_models.tasks import build_models_from_data_file, clean_data_from_source

TAGS = set("slow")


class TestRunTasks(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()
        InitializeDataProviders.load()

    @patch("dataproviders.models.DataFetch.execute_on_save_methods", Mock())
    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    def test_clean_data_from_data_fetch(self):
        data_file, user, data_provider, endpoint, data = self.build_test_data()
        data_fetch = DataFetch.objects.create(endpoint=endpoint, data_file_from_source=data_file, user=user)
        self.assertIsNone(DataFile.objects.first())
        clean_data_from_source(data_fetch.pk, is_from_file_upload=False)
        self.assertIsNotNone(DataFile.objects.first())

    @patch("dataproviders.models.DataFileUpload.execute_on_save_methods", Mock())
    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    def test_clean_data_from_data_file_upload(self):
        data_file, user, data_provider, endpoint, data = self.build_test_data()
        data_file_download = DataFileUpload.objects.create(data_provider=data_provider, data_file_from_source=data_file,
                                                           user=user)
        self.assertIsNone(DataFile.objects.first())
        clean_data_from_source(data_file_download.pk, is_from_file_upload=True)
        self.assertIsNotNone(DataFile.objects.first())

    @patch("dataproviders.models.DataFetch.execute_on_save_methods", Mock())
    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    def test_build_data_from_data_fetch(self):
        data_file, user, data_provider, endpoint, data = self.build_test_data()
        data_fetch = DataFetch.objects.create(endpoint=endpoint, data_file_from_source=data_file, user=user)
        transform_files_to_data.create_data_file(data, user, data_fetch)
        build_models_from_data_file(data_fetch.pk)
        model = get_dynamic_model("activity")
        self.assertIsNotNone(model)

    @patch("dataproviders.models.DataFileUpload.execute_on_save_methods", Mock())
    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    def test_build_data_from_data_file_upload(self):
        data_file, user, data_provider, endpoint, data = self.build_test_data()
        data_file_upload = DataFileUpload.objects.create(data_provider=data_provider, data_file_from_source=data_file,
                                                         user=user)
        transform_files_to_data.create_data_file(data, user, data_file_upload, label_info={"root_label": "activity"})
        build_models_from_data_file(data_file_upload.pk)
        model = get_dynamic_model("activity")
        self.assertIsNotNone(model)

    def build_test_data(self):
        user = User.objects.create(username="test1")
        data_provider = DataProvider.objects.get(provider_name="strava")
        DataProviderUser.objects.create(data_provider=data_provider, user=user)
        endpoint = Endpoint.objects.get(data_provider=data_provider, endpoint_name="activity")
        data = data_fetch_json_strava_activity()
        data_str = JsonUtils.dumps(data)
        data_file = django_file_utils.convert_str_to_file(data_str, filetype=django_file_utils.FileType.JSON)
        return data_file, user, data_provider, endpoint, data

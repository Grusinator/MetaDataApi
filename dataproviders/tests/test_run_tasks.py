from unittest.mock import patch

import django
from django.contrib.auth.models import User
from django.test import TransactionTestCase

import dataproviders.tasks as tasks
from MetaDataApi.tests.utils_for_testing.utils_for_testing import get_method_path
from dataproviders.models import DataProvider, DataProviderUser
from dataproviders.services.initialize_data_providers import InitializeDataProviders


class TestRunTasks(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()
        InitializeDataProviders.load()

    def test_fetch_data_for_each_user(self):
        user = User.objects.create(username="test1")
        dp = DataProvider.objects.get(provider_name="strava")
        DataProviderUser.objects.create(data_provider=dp, user=user)

        with patch(get_method_path(tasks.fetch_data_from_endpoint) + ".delay") as mock_method:
            tasks.fetch_data_for_each_user()
        mock_method.assert_called()

from unittest.mock import Mock

import django
from django.contrib.auth.models import User
from django.test import TransactionTestCase

import dataproviders.tasks as tasks
from dataproviders.models import DataProvider, DataProviderUser
from dataproviders.services.initialize_data_providers import InitializeDataProviders


class TestRunTasks(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()
        InitializeDataProviders.load()
        tasks.fetch_data_from_endpoint = Mock()

    def test_fetch_data_for_each_user(self):
        user = User.objects.create(username="test1")
        dp = DataProvider.objects.get(provider_name="strava")
        DataProviderUser.objects.create(data_provider=dp, user=user)
        tasks.fetch_data_for_each_user()
        tasks.fetch_data_from_endpoint.delay.assert_called()

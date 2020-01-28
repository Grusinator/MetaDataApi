import unittest
from unittest.mock import MagicMock

import django
from django.contrib.auth.models import User
from django.test import TransactionTestCase

import dataproviders.tasks as tasks
from dataproviders.models import DataProvider, DataProviderUser
from dataproviders.services import oauth
from dataproviders.services.initialize_data_providers import InitializeDataProviders


class TestOauth(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()
        InitializeDataProviders.load()

    @unittest.skip("needs more mocking")
    def test_access_token(self):
        request = MagicMock()
        return_value = {"access_token": "test2", "refresh_token": "refresh_token", "expires_in": 300}
        oauth.request_access_token = MagicMock(return_value=return_value)
        data_provider_user = oauth.handle_oath_redirect(request)
        self.assertEqual(data_provider_user.access_token, "")

    def test_refresh_token(self):
        return_value = {"access_token": "test2", "refresh_token": "refresh_token", "expires_in": 300}
        oauth.request_refresh_token = MagicMock(return_value=return_value)
        # We dont want to create a celery task, just test the method.
        DataProviderUser.execute_on_save_methods = MagicMock()
        user = User.objects.create(username="test1")
        dp = DataProvider.objects.get(provider_name="strava")
        DataProviderUser.objects.create(data_provider=dp, user=user, access_token="test1",
                                        refresh_token="refresh_token", expires_in=300)
        tasks.refresh_access_token(dp.provider_name, user.pk)
        dpu = DataProviderUser.objects.get(data_provider=dp, user=user)
        self.assertEqual(dpu.access_token, "test2")

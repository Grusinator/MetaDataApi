from unittest.mock import MagicMock

import django
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from dataproviders.models import DataProviderUser, DataProvider
from dataproviders.models.DataProviderUser import data_provider_user_save_methods
from dataproviders.services import InitializeDataProviders


class TestDataProviderUser(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDataProviderUser, cls).setUpClass()
        django.setup()

    def setUp(self):
        InitializeDataProviders.load()

    def test_celery_task_is_created_on_save(self):
        debug_task = MagicMock()
        # make sure that there is only this one celery task to be executed on save
        [data_provider_user_save_methods.remove(elm) for elm in data_provider_user_save_methods]
        data_provider_user_save_methods.append(debug_task)
        user = User.objects.create(username="test1")
        dp = DataProvider.objects.get(provider_name="strava")
        DataProviderUser.objects.create(data_provider=dp, user=user, access_token="test1",
                                        refresh_token="refresh_token", expires_in=300)
        debug_task.assert_called_once()

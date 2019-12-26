import unittest

import django
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from dataproviders.models import DataProvider, DataProviderUser
from dataproviders.models.initialize_data_providers import InitializeDataProviders
from dataproviders.tasks import fetch_all_data_from_providers


class TestRunTasks(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()

        InitializeDataProviders.load()

    def test_some(self):
        fetch_all_data_from_providers()

    @unittest.skip("cant test celery tasks")
    def test_other(self):
        user = User.objects.create(
            username="test1"
        )
        dp = DataProvider.objects.get(provider_name="strava")
        DataProviderUser.objects.create(
            data_provider=dp,
            user=user,
        )
        # fetch_all_data_from_data_provider_user(user.pk)

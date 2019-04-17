import unittest

import django
from django.test import TransactionTestCase


class test_ouraOauthAuthorizeFlow(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(test_ouraOauthAuthorizeFlow, cls).setUpClass()
        django.setup()

    @unittest.skip
    def test_read_data_from_endpoint_correctly(self):
        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders
        InitializeDataProviders.load()

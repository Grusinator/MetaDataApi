import django
from django.test import TransactionTestCase


class TestHttpConfig(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestHttpConfig, cls).setUpClass()
        django.setup()

    def setUp(self) -> None:
        from dataproviders.models import HttpConfig, DataProvider
        self.data_provider = DataProvider.objects.create(provider_name="dummy")
        self.http = HttpConfig.objects.create(
            data_provider=self.data_provider,
            header=[{"test": 2}],
            url_encoded_params=[{"test": "e"}, ],
            body_type="fit",
            body_content="muscles",
            request_type="proteins"
        )

    def test_JSONField_read(self):
        data = self.http.header
        expected = [{"test": 2}]
        self.assertEqual(expected, data)

    def test_JSONField_write(self):
        expected = [{"test": "test2"}]
        self.http.header = expected
        self.http.save()
        data = self.http.header
        self.assertEqual(expected, data)

import django
from django.test import TransactionTestCase


class TestHttpConfig(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestHttpConfig, cls).setUpClass()
        django.setup()

    def setUp(self) -> None:
        from MetaDataApi.dataproviders.models import HttpConfig, DataProvider
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

    def test_deserialize_http(self):
        data = {
            "http_config": {
                "data_provider": {
                    "provider_name": "test"
                },
                "header": {
                    "User-Agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
                    "X-Auth-Token": "{AuthToken:}",
                    "Content-Type": "application/json"
                },
                "url_encoded_params": {
                    "d": "a",
                    "c": "t"
                },
            }
        }

        from MetaDataApi.dataproviders.models import HttpConfig
        obj = HttpConfig.deserialize(data=data, depth=2,
                                     exclude=("dataproviderprofile", "data_provider", "data_provider_node"))
        self.assertEqual(obj, None)

    def test_serialize_http(self):
        expected = self.build_http_expected_json()

        http = self.build_http_model_objects()

        res = http.serialize(exclude=("body_type", "body_content", "data_provider", "request_type"))
        self.assertEqual(res, expected)

    def test_http_serializer_deserialize(self):
        from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
        data = self.build_http_expected_json()
        serializer = HttpConfigSerializer(data=data)
        if not serializer.is_valid():
            raise Exception(f"could not deserialize, due to error: {serializer.errors}")
        self.assertEqual(serializer.validated_data, data)

    def test_http_serializer_serialize(self):
        from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
        obj = self.build_http_model_objects()
        data = HttpConfigSerializer(obj).data
        self.assertEqual(data, self.build_http_expected_json())

    def build_http_model_objects(self):
        from MetaDataApi.dataproviders.models import DataProvider
        data_provider = DataProvider.objects.create(
            provider_name="test"
        )
        from MetaDataApi.dataproviders.models import HttpConfig
        http = HttpConfig.objects.create(
            data_provider=data_provider,
            url_encoded_params={
                "d": "a",
                "c": "t"
            },
            header={
                "User-Agent": "Tinder",
                "Content-Type": "application-json"
            },
        )
        return http

    def build_http_expected_json(self):
        expected = {
            "header": {
                "User-Agent": "Tinder",
                "Content-Type": "application-json"
            },
            "url_encoded_params": {
                "d": "a",
                "c": "t"
            },
        }
        return expected

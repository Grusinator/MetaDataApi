import django
from django.test import TransactionTestCase


class TestHttpConfigSerializer(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestHttpConfigSerializer, cls).setUpClass()
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

    def test_http_dynamic_serializer_deserialize(self):
        data = self.build_http_expected_json()
        exp_obj = self.build_http_model_objects()

        from MetaDataApi.dataproviders.models import HttpConfig
        validated_data = HttpConfig.deserialize(data=data, max_depth=0,
                                                exclude=("dataproviderprofile", "data_provider", "data_provider_node"))
        obj = HttpConfig.create_object_from_validated_data(validated_data)
        self.assertEqual(exp_obj.header, obj.header)
        self.assertEqual(exp_obj.url_encoded_params, obj.url_encoded_params)

    def test_http_dynamic_serializer_serialize(self):
        expected = self.build_http_expected_json()

        http = self.build_http_model_objects()

        res = http.serialize(exclude_labels=("body_type", "body_content", "data_provider", "request_type"))
        self.assertEqual(res, expected)

    def test_http_static_serializer_deserialize(self):
        from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
        data = self.build_http_expected_json()
        serializer = HttpConfigSerializer(data=data)
        if not serializer.is_valid():
            raise Exception(f"could not deserialize, due to error: {serializer.errors}")
        self.assertEqual(serializer.validated_data, data)

    def test_http_static_serializer_serialize(self):
        from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
        obj = self.build_http_model_objects()
        data = HttpConfigSerializer(obj).data
        self.assertDictEqual(data, self.build_http_expected_json())

    def test_http_static_meta_serializer_deserialize(self):
        from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
        data = self.build_http_expected_json()
        MetaHttpConfigSerializer = HttpConfigSerializer.build_from_metaclass()
        serializer = MetaHttpConfigSerializer(data=data)
        if not serializer.is_valid():
            raise Exception(f"could not deserialize, due to error: {serializer.errors}")
        self.assertEqual(serializer.validated_data, data)

    def test_http_static_meta_serializer_serialize(self):
        from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
        obj = self.build_http_model_objects()
        data = HttpConfigSerializer.build_from_metaclass()(obj).data
        self.assertDictEqual(data, self.build_http_expected_json())

    def test_if_dynamic_serializer_class_is_equal_to_static(self):
        from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
        stat = HttpConfigSerializer
        from MetaDataApi.dataproviders.models import HttpConfig
        dyna = HttpConfig.build_serializer(self.build_default_filter(max_depth=2))
        self.assert_meta_equal(dyna, stat)

    def test_meta_static_dynamic_properties_equal(self):
        from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer

        stat = HttpConfigSerializer.build_properties()
        from MetaDataApi.dataproviders.models import HttpConfig
        dyna = HttpConfig.build_properties(self.build_default_filter())
        self.assertEqual(type(stat), type(dyna))
        self.assertEqual(type(stat["header"]), type(dyna["header"]))
        self.assertEqual(type(stat["url_encoded_params"]), type(dyna["url_encoded_params"]))
        self.assertEqual(stat["Meta"].model, dyna["Meta"].model)

    def test_if_dynamic_serializer_class_is_equal_to_static_metaclass(self):
        from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
        stat = HttpConfigSerializer.build_from_metaclass()
        from MetaDataApi.dataproviders.models import HttpConfig
        dyna = HttpConfig.build_serializer(self.build_default_filter())
        self.assert_meta_equal(dyna, stat)

    def assert_meta_equal(self, dyna, stat):
        self.assertSetEqual(set(stat.Meta.fields), set(dyna.Meta.fields))
        self.assertEqual(stat.Meta.model, dyna.Meta.model)

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

    @staticmethod
    def build_default_filter(max_depth=0):
        from MetaDataApi.dataproviders.models.SerializableModelFilter import SerializableModelFilter
        filter = SerializableModelFilter(
            max_depth=max_depth,
            exclude_labels=(
                "data_provider",
                'body_type',
                'body_content',
                'request_type'
            )
        )
        return filter

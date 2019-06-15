from unittest import TestCase

import django


class TestSerializableModel(TestCase):

    @classmethod
    def setUpClass(cls):
        django.setup()
        from MetaDataApi.dataproviders.models import DataProvider
        cls.model = DataProvider

    def test_build_serializer(self):
        serializer = self.model.build_serializer()
        self.assertEqual(serializer.Meta.model, self.model)
        expected_ignore = ['id', 'endpoints', 'http_config', 'oauth_config']
        self.assertListEqual(expected_ignore, serializer.Meta.ignore)

        for name in ['endpoints', 'http_config', 'oauth_config']:
            subserializer = self.assert_sub_serializer(name, serializer)
            from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
            self.assertIsInstance(subserializer.Meta.model.data_provider, ForwardManyToOneDescriptor)
            if name is "endpoints":
                dump_serializer = self.assert_sub_serializer("data_dumps", subserializer)

    def assert_sub_serializer(self, name, serializer):
        subserializer = getattr(serializer, name)
        from rest_framework.serializers import SerializerMetaclass
        self.assertIsInstance(subserializer, SerializerMetaclass)
        self.assertIn('id', subserializer.Meta.ignore)
        return subserializer

    def test_build_serializer_ignore(self):
        serializer = self.model.build_serializer(ignore=('oauth_config',))
        self.assertEqual(serializer.Meta.model, self.model)
        expected_ignore = ['id', 'endpoints', 'http_config', 'oauth_config']
        self.assertListEqual(expected_ignore, serializer.Meta.ignore)
        self.assertFalse(hasattr(serializer, "oauth_config"))
        self.assertTrue(hasattr(serializer, "http_config"))
        self.assertTrue(hasattr(serializer, "endpoints"))

    def test_build_serializer_depth_0(self):
        serializer = self.model.build_serializer(depth=0)
        self.assertFalse(hasattr(serializer, "oauth_config"))
        self.assertFalse(hasattr(serializer, "http_config"))
        self.assertFalse(hasattr(serializer, "endpoints"))

    def test_build_serializer_depth_1(self):
        serializer = self.model.build_serializer(depth=1)
        for name in ['endpoints', 'http_config', 'oauth_config']:
            subserializer = self.assert_sub_serializer(name, serializer)
            if name is "endpoints":
                self.assertFalse(hasattr(subserializer, "data_dumps"))

    def test_build_serializer_depth_2(self):
        serializer = self.model.build_serializer(depth=2)
        for name in ['endpoints', 'http_config', 'oauth_config']:
            subserializer = self.assert_sub_serializer(name, serializer)
            if name is "endpoints":
                self.assertTrue(hasattr(subserializer, "data_dumps"))

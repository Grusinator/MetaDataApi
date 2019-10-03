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
        expected_exclude = ['id', 'endpoints', 'http_config', 'oauth_config']
        self.assertNotIn(expected_exclude, serializer.Meta.fields)

        for name in ['endpoints', 'http_config', 'oauth_config']:
            sub_serializer = self.assert_sub_serializer(name, serializer)
            from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
            self.assertIsInstance(sub_serializer.Meta.model.data_provider, ForwardManyToOneDescriptor)
            if name is "endpoints":
                dump_serializer = self.assert_sub_serializer("data_dumps", sub_serializer)

    def assert_sub_serializer(self, name, serializer):
        sub_serializer = getattr(serializer, name)
        from rest_framework.serializers import SerializerMetaclass
        self.assertIsInstance(sub_serializer, SerializerMetaclass)
        return sub_serializer

    def test_build_serializer_exclude(self):
        serializer = self.model.build_serializer(exclude=('oauth_config',))
        self.assertEqual(serializer.Meta.model, self.model)
        self.assertIn('endpoints', serializer.Meta.fields)
        self.assertIn('http_config', serializer.Meta.fields)
        self.assertFalse(hasattr(serializer, "oauth_config"))
        self.assertTrue(hasattr(serializer, "http_config"))
        self.assertTrue(hasattr(serializer, "endpoints"))

    def test_build_serializer_depth_0(self):
        serializer = self.model.build_serializer(max_depth=0)
        self.assertTrue(hasattr(serializer, "Meta"))
        self.assertFalse(hasattr(serializer, "oauth_config"))
        self.assertFalse(hasattr(serializer, "http_config"))
        self.assertFalse(hasattr(serializer, "endpoints"))

    def test_build_serializer_depth_1(self):
        serializer = self.model.build_serializer(max_depth=1)
        for name in ['endpoints', 'http_config', 'oauth_config']:
            sub_serializer = self.assert_sub_serializer(name, serializer)
            if name is "endpoints":
                self.assertFalse(hasattr(sub_serializer, "data_dumps"))

    def test_build_serializer_depth_2(self):
        serializer = self.model.build_serializer(max_depth=2)
        for name in ['endpoints', 'http_config', 'oauth_config']:
            sub_serializer = self.assert_sub_serializer(name, serializer)
            if name is "endpoints":
                self.assertTrue(hasattr(sub_serializer, "data_dumps"))

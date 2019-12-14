import unittest
from unittest import TestCase

import django


class TestSerializableModel(TestCase):

    @classmethod
    def setUpClass(cls):
        django.setup()
        from dataproviders.models import DataProvider
        cls.model = DataProvider

    @unittest.skip("move to Serializer project, failing due to known issues")
    def test_build_serializer(self):
        serializer = self.model.build_serializer(self.build_default_test_filter(max_depth=2))
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

    @unittest.skip("move to Serializer project, failing due to known issues")
    def test_build_serializer_exclude(self):
        serializer = self.model.build_serializer(self.build_default_test_filter(exclude_labels=('oauth_config',)))
        self.assertEqual(serializer.Meta.model, self.model)
        self.assertIn('endpoints', serializer.Meta.fields)
        self.assertIn('http_config', serializer.Meta.fields)
        self.assertFalse(hasattr(serializer, "oauth_config"))
        self.assertTrue(hasattr(serializer, "http_config"))
        self.assertTrue(hasattr(serializer, "endpoints"))

    def test_build_serializer_depth_0(self):
        serializer = self.model.build_serializer(self.build_default_test_filter(max_depth=0))
        self.assertTrue(hasattr(serializer, "Meta"))
        self.assertFalse(hasattr(serializer, "oauth_config"))
        self.assertFalse(hasattr(serializer, "http_config"))
        self.assertFalse(hasattr(serializer, "endpoints"))

    @unittest.skip("move to Serializer project, failing due to known issues")
    def test_build_serializer_depth_1(self):
        serializer = self.model.build_serializer(self.build_default_test_filter(max_depth=1))
        for name in ['endpoints', 'http_config', 'oauth_config']:
            sub_serializer = self.assert_sub_serializer(name, serializer)
            if name is "endpoints":
                self.assertFalse(hasattr(sub_serializer, "data_dumps"))

    @unittest.skip("move to Serializer project, failing due to known issues")
    def test_build_serializer_depth_2(self):
        serializer = self.model.build_serializer(self.build_default_test_filter(max_depth=2))
        for name in ['endpoints', 'http_config', 'oauth_config']:
            sub_serializer = self.assert_sub_serializer(name, serializer)
            if name is "endpoints":
                self.assertTrue(hasattr(sub_serializer, "data_dumps"))

    def build_default_test_filter(self, max_depth=0, exclude_labels=(), start_object_name="data_provider"):
        from generic_serializer import SerializableModelFilter
        default_exclude = ("data_provider_node", "dataproviderprofile")
        return SerializableModelFilter(
            max_depth=max_depth,
            exclude_labels=exclude_labels + default_exclude,
            start_object_name=start_object_name)

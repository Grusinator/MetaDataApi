import unittest

from django.test import TransactionTestCase


class TestBaseRdfsObject(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestBaseRdfsObject, cls).setUpClass()
        # django.setup()

    def test_get_all_schema_items_of_type_stringattribute(self):
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider import Endpoint
        from MetaDataApi.metadata.rdfs_models.descriptors import StringAttributeDescriptor
        descriptors = Endpoint.get_all_schema_items_of_type(StringAttributeDescriptor)
        descriptor_labels = list(map(lambda x: x.label, descriptors))
        descriptor_labels.sort()
        expected = ["api_type", "endpoint_name", "endpoint_url"]
        self.assertListEqual(expected, descriptor_labels)

    def test_get_all_schema_items_of_type_relation(self):
        from MetaDataApi.metadata.rdfs_models.descriptors import ObjectRelationDescriptor
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import gDataProvider
        descriptors = gDataProvider.get_all_schema_items_of_type(ObjectRelationDescriptor)
        descriptor_labels = list(map(lambda x: x.label, descriptors))
        descriptor_labels.sort()
        expected = ["endpoints"]
        self.assertListEqual(expected, descriptor_labels)

    def test_get_all_schema_items_of_type_base_attribute(self):
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider import Endpoint
        from MetaDataApi.metadata.rdfs_models.descriptors.attributes.base_attribute_descriptor import \
            BaseAttributeDescriptor
        descriptors = Endpoint.get_all_schema_items_of_type(BaseAttributeDescriptor)
        descriptor_labels = list(map(lambda x: x.label, descriptors))
        descriptor_labels.sort()
        expected = ["api_type", "endpoint_name", "endpoint_url"]
        self.assertListEqual(expected, descriptor_labels)

    unittest.skip("move to other method")
    def test_get_attribute_set_diffence(self):
        from MetaDataApi.metadata.rdfs_models.descriptors.attributes.base_attribute_descriptor import \
            BaseAttributeDescriptor
        test_data = [
            # new , existing
            (1, [1, 2, 3]),
            ([1], [1, 2, 3]),
            ([4], [1, 2, 3]),
            (4, [1, 2, 3]),
            ([], [1, 2, 3])
        ]
        expected = [
            [],
            [],
            [4],
            [4],
            []
        ]
        for test, expected in zip(test_data, expected):
            output = BaseAttributeDescriptor.get_attribute_set_difference(*test)
            self.assertEqual(output, expected, msg=str(test))

    @unittest.skip
    def test_build_json_from_att_names(self):
        self.fail()

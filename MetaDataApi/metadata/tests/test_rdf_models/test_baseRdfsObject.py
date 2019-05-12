import unittest

from django.test import TransactionTestCase


class TestBaseRdfsObject(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestBaseRdfsObject, cls).setUpClass()
        # django.setup()

    @unittest.skip
    def test_get_base_object(self):
        self.fail()

    @unittest.skip
    def test_create_self(self):
        self.fail()

    @unittest.skip
    def test_update_from_json(self):
        self.fail()

    @unittest.skip
    def test_getAttribute(self):
        self.fail()

    @unittest.skip
    def test_get_attribute_value(self):
        self.fail()

    @unittest.skip
    def test_getAttributes(self):
        self.fail()

    @unittest.skip
    def test_get_attribute_values(self):
        self.fail()

    @unittest.skip
    def test_setAttribute(self):
        self.fail()

    @unittest.skip
    def test_getParrentObjects(self):
        self.fail()

    @unittest.skip
    def test_getChildObjects(self):
        self.fail()

    @unittest.skip
    def test_setChildObjects(self):
        self.fail()

    @unittest.skip
    def test_value_to_json(self):
        self.fail()

    @unittest.skip
    def test_existing_objects_as_json_set(self):
        self.fail()

    @unittest.skip
    def test_create_relations(self):
        self.fail()

    @unittest.skip
    def test_get_json_set_diffence(self):
        self.fail()

    def test_get_attribute_set_diffence(self):
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.base_rdfs_object import BaseRdfsObject
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
            output = BaseRdfsObject.get_attribute_set_difference(*test)
            self.assertEqual(output, expected, msg=str(test))

    @unittest.skip
    def test_build_json_from_att_names(self):
        self.fail()

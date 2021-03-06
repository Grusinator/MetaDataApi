import unittest
from datetime import datetime

import django
from django.test import TransactionTestCase


class TestAttribute(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestAttribute, cls).setUpClass()
        django.setup()

    @unittest.skip
    def test_datatype_to_data_object(self):
        self.fail()

    @unittest.skip
    def test_exists_by_label(self):
        self.fail()

    @unittest.skip
    def test_exists(self):
        self.fail()

    @unittest.skip
    def test_assert_data_type(self):
        self.fail()

    def test_all_instances(self):
        from metadata.tests import LoadTestData
        schema = LoadTestData.init_foaf()
        from metadata.models import SchemaNode, SchemaAttribute
        obj = SchemaNode(label="test", schema=schema)
        obj.save()

        from metadata.models import BaseAttribute, Node
        from metadata.models import FileAttribute
        from metadata.models import ImageAttribute
        for InstanceType in set(BaseAttribute.get_all_instance_types()) - {FileAttribute,
                                                                           ImageAttribute}:
            data_type = InstanceType.get_data_type()
            att = SchemaAttribute(
                label="test_%s" % str(data_type),
                data_type=data_type,
                object=obj,
            )
            att.save()

            obj_inst = Node(base=obj)
            obj_inst.save()

            value = data_type(2011, 4, 3) if data_type is datetime else data_type()

            att_inst = InstanceType(
                value=value,
                base=att,
                object=obj_inst
            )
            att_inst.save()

            instances = BaseAttribute.get_all_instances_from_base(att)

            self.assertListEqual([att_inst], instances)

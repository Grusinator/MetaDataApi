import unittest

import django
from django.test import TransactionTestCase


class TestObjectInstance(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestObjectInstance, cls).setUpClass()
        django.setup()

    @unittest.skip
    def test_get_att_inst(self):
        self.fail()

    def test_equal(self):
        from MetaDataApi.metadata.tests import LoadTestData
        foaf = LoadTestData.init_foaf_person()

        from MetaDataApi.metadata.models import ObjectInstance
        from MetaDataApi.metadata.models import Attribute
        first_name = Attribute.objects.get(label="first_name")
        peter = ObjectInstance(base=foaf)
        peter.save()
        peter.create_att_inst(first_name, "peter")

        anders = ObjectInstance(base=foaf)
        anders.save()
        anders.create_att_inst(first_name, "peter")

        self.assertIsNot(anders, peter)
        self.assertEqual(peter, anders)
        self.assertEqual(peter, {("first_name", "peter")})
        self.assertIsNot(anders, {("first_name", "peter")})

    def test_get_child_and_parrent_obj_instance_with_relation(self):
        from MetaDataApi.metadata.models import ObjectInstance, ObjectRelationInstance, ObjectRelation

        from MetaDataApi.metadata.tests import LoadTestData
        foaf = LoadTestData.init_foaf_person()

        parrent = ObjectInstance(base=foaf)
        parrent.save()

        child = ObjectInstance(base=foaf)
        child.save()

        rel = ObjectRelationInstance(
            base=ObjectRelation.objects.get(label="knows"),
            from_object=parrent,
            to_object=child
        )
        rel.save()

        found_child = parrent.get_child_obj_instances_with_relation(rel.base.label)

        found_parrent = child.get_parrent_obj_instances_with_relation(rel.base.label)

        self.assertEqual(child, found_child[0])
        self.assertEqual(parrent, found_parrent[0])

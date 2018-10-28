import django
from django.test import TestCase, TransactionTestCase
import collections
from django.db import transaction


# TODO: Configure your database in settings.py and sync before running tests.


class TestRdfInstanceService(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()
        super(TestRdfInstanceService, cls).setUpClass()

    def test_export_rdf(self):
        from MetaDataApi.metadata.services import (
            RdfSchemaService, RdfInstanceService)

        from MetaDataApi.metadata.models import (
            Object, Schema, Attribute, ObjectRelation
        )

        from MetaDataApi.datapoints.models import (
            GenericAttributeInstance, RawData, CategoryTypes,
            ObjectInstance,
            ObjectRelationInstance,
            GenericAttributeInstance,
            FloatAttributeInstance,
            StringAttributeInstance)

        schema_label = "friend_of_a_friend"

        service = RdfSchemaService()
        # just take foaf
        service.write_to_db(rdf_url="http://xmlns.com/foaf/0.1/")

        foaf_atts = Attribute.objects.filter(
            object__schema__label=schema_label)
        s = list(filter(lambda x: x.label, foaf_atts))

        foaf_person = service.get_foaf_person()
        foaf_name = Attribute.objects.get(label="first_name",
                                          object__schema__label=schema_label)

        foaf_knows = ObjectRelation.objects.get(label="knows",
                                                schema__label=schema_label)

        b1 = ObjectInstance(base=foaf_person)
        b2 = ObjectInstance(base=foaf_person)
        b1.save()
        b2.save()

        name1 = StringAttributeInstance(base=foaf_name, object=b1, value="B1")
        name2 = StringAttributeInstance(base=foaf_name, object=b2, value="B2")
        name1.save()
        name2.save()

        rel1 = ObjectRelationInstance(
            base=foaf_knows, from_object=b1, to_object=b2)

        rel1.save()

        objects = [b1, b2, name1, name2, rel1]

        read_service = RdfInstanceService()
        rdf_file = read_service.export_instances_to_rdf_file(
            schema_label, objects)

        self.assertIsNotNone(rdf_file.url)

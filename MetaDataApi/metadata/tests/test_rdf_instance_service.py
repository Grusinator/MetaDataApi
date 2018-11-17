import django
from django.test import TestCase, TransactionTestCase
import collections
from django.db import transaction

from MetaDataApi.metadata.tests import TestDataInits
# TODO: Configure your database in settings.py and sync before running tests.


class TestRdfInstanceService(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()
        super(TestRdfInstanceService, cls).setUpClass()

    def test_(self):
        from MetaDataApi.metadata.services import (
            RdfSchemaService, RdfInstanceService)

        from MetaDataApi.metadata.models import (
            Object, Schema, Attribute, ObjectRelation
        )

        from MetaDataApi.metadata.models import (
            RawData, CategoryTypes,
            ObjectInstance,
            ObjectRelationInstance,

            FloatAttributeInstance,
            StringAttributeInstance)

        TestDataInits.init_foaf()

        service = RdfInstanceService()

        schema_label = "friend_of_a_friend"

        schema = service._try_get_item(Schema(label=schema_label))

        foaf_atts = Attribute.objects.filter(
            object__schema=schema)
        s = list(filter(lambda x: x.label, foaf_atts))

        foaf_person = service.get_foaf_person()
        foaf_name = Attribute.objects.get(label="first_name",
                                          object__schema=schema)

        foaf_knows = ObjectRelation.objects.get(label="knows",
                                                schema=schema)

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

        rdf_file = service.export_instances_to_rdf_file(
            schema, objects)

        self.assertIsNotNone(rdf_file.url)

import django
from django.test import TransactionTestCase

from MetaDataApi.metadata.tests.data import LoadTestData


# TODO: Configure your database in settings.py and sync before running tests.


class TestRdfInstanceService(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestRdfInstanceService, cls).setUpClass()
        django.setup()

    def test_(self):
        from MetaDataApi.metadata.services import (
            RdfInstanceService)

        from MetaDataApi.metadata.models import (
            Schema, SchemaAttribute, SchemaEdge
        )

        from MetaDataApi.metadata.models import (
            Node,
            Edge,

            StringAttribute)

        LoadTestData.init_foaf()

        service = RdfInstanceService()

        schema_label = "friend_of_a_friend"

        schema = service.do_meta_item_exists(Schema(label=schema_label))

        foaf_atts = SchemaAttribute.objects.filter(
            object__schema=schema)
        s = list(filter(lambda x: x.label, foaf_atts))

        foaf_person = service.get_foaf_person()
        foaf_name = SchemaAttribute.objects.get(label="first_name",
                                                object__schema=schema)

        foaf_knows = SchemaEdge.objects.get(label="knows",
                                            schema=schema)

        b1 = Node(base=foaf_person)
        b2 = Node(base=foaf_person)
        b1.save()
        b2.save()

        name1 = StringAttribute(base=foaf_name, object=b1, value="B1")
        name2 = StringAttribute(base=foaf_name, object=b2, value="B2")
        name1.save()
        name2.save()

        rel1 = Edge(
            base=foaf_knows, from_object=b1, to_object=b2)

        rel1.save()

        objects = [b1, b2, name1, name2, rel1]

        rdf_file = service.export_instances_to_rdf_file(
            schema, objects)

        self.assertIsNotNone(rdf_file.url)

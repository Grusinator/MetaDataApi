# Create your tests here.

import django
import graphene
import mutant.contrib.numeric.models
from django.test import TransactionTestCase
from mutant.models import ModelDefinition

from dataproviders.services import InitializeDataProviders
from dynamic_models import schema


class TestGrapheneSchema(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()
        InitializeDataProviders.load()
        create_dummy_model_def()

    def test_create_query(self):
        query = schema.create_query()
        self.assertIs(type(query), graphene.ObjectType)

    def test_create_types_for_all_dynamic_models(self):
        graphene_types = schema.create_types_for_all_dynamic_models()
        self.assertEqual(graphene_types[0]._meta.name, "dummy")

    def test_build_properties(self):
        graphene_types = schema.create_types_for_all_dynamic_models()
        properties = schema.build_query_properties(graphene_types)
        self.assertTrue("dummy" in properties.keys())
        self.assertTrue("all_dummys" in properties.keys())


def create_dummy_model_def():
    model_def, created = ModelDefinition.objects.get_or_create(
        app_label="json2model",
        object_name="dummy",
        defaults={'fields': []}
    )
    field_schema, created = mutant.contrib.numeric.models.BigIntegerFieldDefinition.objects.get_or_create(
        name="dummy_field",
        model_def=model_def,
        blank=True,
        null=True
    )

# Create your tests here.
import unittest

import django
import graphene
import mutant.contrib.numeric.models
from django.test import TransactionTestCase
from mutant.models import ModelDefinition

from dynamic_models import schema
from dynamic_models.schema import build_dynamic_model_query


class TestGrapheneSchema(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()
        cls.create_dummy_model_def()

    def test_create_query(self):
        query = build_dynamic_model_query()
        schema = graphene.Schema(query=query, mutation=None)

    @unittest.skip
    def test_create_types_for_all_dynamic_models(self):
        graphene_types = schema.create_types_for_all_dynamic_models()
        self.assertEqual(graphene_types[0]._meta.name, "dummy")

    @unittest.skip("cant run in sequence, very strange")
    def test_build_properties(self):
        graphene_types = schema.create_types_for_all_dynamic_models()
        properties = schema.build_query_properties(graphene_types)
        self.assertTrue("dummy" in properties.keys())
        self.assertTrue("all_dummys" in properties.keys())

    @staticmethod
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

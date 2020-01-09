# Create your tests here.
import django
from django.test import TransactionTestCase
from mutant.models import ModelDefinition

from dynamic_models.schema import create_query


class TestDynamicGraphql(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()

    def test_create_query(self):
        model = ModelDefinition.objects.create(
            app_label="dynamic_models", object_name="test"
        )
        all_models = ModelDefinition.objects.all()
        Query = create_query()
        # self.assertEqual(type(Query), graphene.ObjectType)
        self.assertIsNotNone(Query)

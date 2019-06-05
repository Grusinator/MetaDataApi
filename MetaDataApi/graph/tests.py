# Create your tests here.
import django
from django.db import models
from django.test import TransactionTestCase


class TestDjangoDynamicModel(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDjangoDynamicModel, cls).setUpClass()
        django.setup()

    def test_simple(self):
        from MetaDataApi.graph.models import ModelSchema
        car_model_schema = ModelSchema.objects.create(name='car')
        Car = car_model_schema.as_model()
        assert issubclass(Car, models.Model)

        # The dynamic model can now be used to create Car instances
        instance = Car.objects.create()
        assert instance.pk is not None

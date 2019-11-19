# Create your tests here.
import unittest

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
        from django.db import models
        from MetaDataApi.graph.models import ModelSchema
        car_model_schema = ModelSchema.objects.create(name='car')
        Car = car_model_schema.as_model()
        assert issubclass(Car, models.Model)

        # The dynamic model can now be used to create Car instances
        instance = Car.objects.create()
        assert instance.pk is not None

    @unittest.skip("check later after merging dynamic model aproach")
    def test_2(self):
        from MetaDataApi.graph.models import ModelSchema, FieldSchema

        car_model_schema = ModelSchema.objects.create(name='car')
        # car_model_schema = ModelSchema.objects.get(name="car")
        Car = car_model_schema.as_model()
        assert issubclass(Car, models.Model)

        # The dynamic model can now be used to create Car instances
        instance = Car.objects.create()
        assert instance.pk is not None

        color_field_schema = FieldSchema.objects.create(name='color', data_type='character')

        color = car_model_schema.add_field(
            color_field_schema,
            null=False,
            unique=False,
            max_length=16
        )

        Car = car_model_schema.as_model()
        red_car = Car.objects.create(color='red')
        assert red_car.color == 'red'

        print(red_car.color)

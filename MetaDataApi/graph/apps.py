from django.apps import AppConfig


class GraphConfig(AppConfig):
    name = 'MetaDataApi.graph'

    def ready(self):
        from MetaDataApi.graph.models import ModelSchema, FieldSchema

        if not ModelSchema.objects.get(name="car"):
            car_model_schema = ModelSchema.objects.create(name='car')
            color_field_schema = FieldSchema.objects.create(name='color', data_type='character')

            color = car_model_schema.add_field(
                color_field_schema,
                null=False,
                unique=False,
                max_length=16
            )

            Car = car_model_schema.as_model()
            red_car = Car.objects.create(color='red')

from MetaDataApi.graph.models import FieldSchema, ModelSchema


class DynamicModelService:

    @classmethod
    def create_from_data(cls, data, root_name):
        model_name = ""
        model_schema = ModelSchema.objects.create(name=model_name)
        Model = model_schema.as_model()

        cls.create_fields_and_related_objects(data, model_schema)
        Model.objects.create()

        color_field_schema = FieldSchema.objects.create(name='color', data_type='character')

        color = model_schema.add_field(
            color_field_schema,
            null=False,
            unique=False,
            max_length=16
        )

    @classmethod
    def create_fields_and_related_objects(cls, data: dict, model_schema):
        for name, value in data.items():
            if isinstance(dict, value):
                pass

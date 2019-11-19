from mutant.models import ModelDefinition, FieldDefinition


class DynamicModelMutantService:
    datatype_map = {
        int: "number",
        str: "character"
    }

    @classmethod
    def create_from_data(cls, root_name, data):
        cls._create_object_iterative(root_name, data)

    @classmethod
    def _create_object_iterative(cls, object_name, data):
        properties, related_objects = cls.split_into_properties_and_reated_objects(data)
        fields = cls._create_fields(properties)
        model_def = cls._create_or_get_model_def(object_name, fields)

        related_instances = cls.create_related_objects(related_objects)

        return cls.create_object_instance(model_def, related_instances, properties)

    @classmethod
    def _create_or_get_model_def(cls, object_name, fields):

        model_def = ModelDefinition.objects.get_or_create(
            app_label='testapp',
            object_name=object_name,
            defaults={'fields': []},  # [CharFieldDefinition(name='char_field', max_length=25)]}
        )

        return model_def

    @classmethod
    def _create_fields(cls, data: dict):
        return [cls._create_field(name, value) for name, value in data.items()]

    @classmethod
    def _create_field(cls, name, value):
        data_type = cls.datatype_map[type(value)]
        field_schema = FieldDefinition.objects.create(name=name, field_type=data_type)
        return field_schema

    @classmethod
    def create_object_instance(cls, model_def, related_instances, properties):
        Model = model_def.model_class()

        return Model.objects.create(**properties, **related_instances)

    @classmethod
    def create_related_objects(cls, data):
        return [cls._create_object_iterative(name, value) for name, value in data.items()]

    @classmethod
    def split_into_properties_and_reated_objects(cls, data):
        properties = {}
        related_instances = {}
        for name, value in data.items():
            if isinstance(value, dict):
                related_instances[name] = value
            else:
                properties[name] = value

        return properties, related_instances

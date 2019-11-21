import datetime

import mutant.contrib.boolean.models
import mutant.contrib.file.models
import mutant.contrib.numeric.models
import mutant.contrib.related.models
import mutant.contrib.temporal.models
import mutant.contrib.text.models
from django.contrib.sessions.backends import file
from mutant.models import ModelDefinition


class DynamicModelMutantService:
    FIELD_TYPES = {
        str: mutant.contrib.text.models.TextFieldDefinition,
        float: mutant.contrib.numeric.models.FloatFieldDefinition,
        bool: mutant.contrib.boolean.models.BooleanFieldDefinition,
        int: mutant.contrib.numeric.models.BigIntegerFieldDefinition,
        file: mutant.contrib.file.models.FilePathFieldDefinition,
        datetime: mutant.contrib.temporal.models.DateTimeFieldDefinition,
        # ('varchar', mutant.contrib.text.models.CharFieldDefinition),
        #
        # ('integer', mutant.contrib.numeric.models.BigIntegerFieldDefinition),
        # ('small_integer', mutant.contrib.numeric.models.SmallIntegerFieldDefinition),
        # ('float', mutant.contrib.numeric.models.FloatFieldDefinition),
        #
        # ('null_boolean', mutant.contrib.boolean.models.NullBooleanFieldDefinition),
        # ('boolean', mutant.contrib.boolean.models.BooleanFieldDefinition),
        #
        # ('file', mutant.contrib.file.models.FilePathFieldDefinition),
        #
        # ('foreign_key', mutant.contrib.related.models.ForeignKeyDefinition),
        # ('one_to_one', mutant.contrib.related.models.OneToOneFieldDefinition),
        # ('many_to_many', mutant.contrib.related.models.ManyToManyFieldDefinition),
        #
        # ('ip_generic', mutant.contrib.web.models.GenericIPAddressFieldDefinition),
        # ('ip', mutant.contrib.web.models.IPAddressFieldDefinition),
        # ('email', mutant.contrib.web.models.EmailFieldDefinition),
        # ('url', mutant.contrib.web.models.URLFieldDefinition),
        #
        # ('date', mutant.contrib.temporal.models.DateFieldDefinition),
        # ('time', mutant.contrib.temporal.models.TimeFieldDefinition),
        # ('datetime', mutant.contrib.temporal.models.DateTimeFieldDefinition),
    }

    @classmethod
    def create_from_data(cls, root_name, data):
        cls._create_object_and_instance_iterative(root_name, data)

    @classmethod
    def _create_object_and_instance_iterative(cls, object_name, data):
        properties, related_objects = cls._split_into_properties_and_related_objects(data)

        model_def = cls._create_or_get_model_def(object_name)
        cls._create_fields(model_def, properties)

        related_instances = cls._create_related_objects_and_instances(model_def, related_objects)

        return cls._create_object_instance(model_def, related_instances, properties)

    @classmethod
    def _create_or_get_model_def(cls, object_name):
        model_def = ModelDefinition.objects.get_or_create(
            app_label='testapp',
            object_name=object_name,
            defaults={'fields': []},  # [CharFieldDefinition(name='char_field', max_length=25)]}
        )
        return model_def[0]

    @classmethod
    def _create_fields(cls, model_def, data: dict):
        return [cls._create_field(model_def, name, value) for name, value in data.items()]

    @classmethod
    def _create_field(cls, model_def, field_name: str, value):
        SpecificFieldDefinition = cls._get_specific_field_def(value)
        field_schema = SpecificFieldDefinition.objects.get_or_create(
            name=field_name,
            model_def=model_def
        )
        return field_schema

    @classmethod
    def _create_object_instance(cls, model_def, related_instances: dict, properties: dict):
        Model = model_def.model_class()
        return Model.objects.create(**properties, **related_instances)

    @classmethod
    def _create_related_objects_and_instances(cls, model_def, data):
        return {name: cls._create_related_object_and_instance(model_def, name, value) for name, value in data.items()}

    @classmethod
    def _split_into_properties_and_related_objects(cls, data):
        properties = {}
        related_instances = {}
        for name, value in data.items():
            if isinstance(value, dict):
                related_instances[name] = value
            else:
                properties[name] = value

        return properties, related_instances

    @classmethod
    def _get_specific_field_def(cls, value):
        return cls.FIELD_TYPES.get(type(value))

    @classmethod
    def _create_related_object_and_instance(cls, model_def, name, value):
        related_instance = cls._create_object_and_instance_iterative(name, value)
        related_object = ModelDefinition.objects.get(object_name=name)
        SpecificRelationFieldDef = cls._get_specific_relation_field_def(value)
        SpecificRelationFieldDef.objects.create(model_def=model_def, name=name, to=related_object)
        return related_instance

    @classmethod
    def _get_specific_relation_field_def(cls, value):
        if isinstance(value, dict):
            return mutant.contrib.related.models.OneToOneFieldDefinition
        elif isinstance(value, list):
            return mutant.contrib.related.models.ManyToManyFieldDefinition

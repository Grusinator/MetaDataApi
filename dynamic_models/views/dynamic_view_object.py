from typing import Union

from json2model.services.dynamic_model.dynamic_model_utils import get_model_def

from dynamic_models.schema import get_field_names, get_fields, attribute_types

exclude = ("id", "user_pk")


class DynamicViewObject:
    def __init__(self, dynamic_data_instance):
        self.inst = dynamic_data_instance
        self.model = type(self.inst)
        self.model_name = self.model.__name__
        self.fields = [FieldViewObject(self.inst, field) for field in get_fields(self.model) if
                       field.name not in exclude]
        self.field_names = [name for name in get_field_names(self.model) if name not in exclude]
        self.meta_object = get_model_def(self.model_name).meta_object

    @property
    def field_values(self):
        return [getattr(self.inst, field_name) for field_name in self.field_names if field_name not in exclude]

    @property
    def id(self):
        return self.inst.pk

    def get_field_value(self, index):
        try:
            return getattr(self.inst, self.field_names[index])
        except Exception:
            return "N/A"


class FieldViewObject:
    def __init__(self, inst, field: Union[attribute_types]):
        self.field = field
        self.value = getattr(inst, self.field.name) or ""
        self.value_short = self.create_short_value()
        self.name = self.field.name
        self.type = type(self.field).__name__

    def create_short_value(self):
        if isinstance(self.value, str) and len(self.value) > 18:
            return f"{self.value[:18]}.."
        else:
            return self.value

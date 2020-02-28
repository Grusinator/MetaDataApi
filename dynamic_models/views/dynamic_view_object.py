from typing import Union

from dynamic_models.schema import get_field_names, get_fields, attribute_types


class DynamicViewObject:
    def __init__(self, dynamic_data_instance):
        self.inst = dynamic_data_instance
        self.model = type(self.inst)
        self.model_name = self.model.__name__
        self.fields = [FieldViewObject(self.inst, field) for field in get_fields(self.model)]
        self.field_names = get_field_names(self.model)
        # self.meta_object = self.inst.meta_object

    @property
    def field_values(self):
        return [getattr(self.inst, field_name) for field_name in self.field_names]

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
        self.name = self.field.name
        self.type = type(self.field).__name__

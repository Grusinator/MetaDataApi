from django.db.models import TextField, IntegerField, FloatField, BooleanField

from dynamic_models.schema import get_all_field_names_of_type

attribute_types = (TextField, IntegerField, FloatField, BooleanField)


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class DynamicViewObject:
    def __init__(self, dynamic_data_instance):
        self.inst = dynamic_data_instance
        self.model = type(self.inst)
        self.field_names = get_all_field_names_of_type(self.model, attribute_types)
        # self.meta_object = self.inst.meta_object

    def __getattr__(self, name):
        number = name[3:]
        if "col" == name[0:3] and is_integer(number):
            return self.get_field_value(int(number))
        else:
            raise AttributeError("use colX")

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

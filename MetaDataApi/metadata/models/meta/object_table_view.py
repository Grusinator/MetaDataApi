from MetaDataApi.metadata.models import Object


class ObjectTableView:
    def __init__(self, obj: Object):
        self.object = obj
        self.max_number_of_atts = 10
        self.selected_attributes = []
        self.instances = []
        self.select_attributes()
        self.select_default_object_instances()

    def select_attributes(self, exclude_type: tuple = ()):
        self.selected_attributes = list(self.object.attributes.all())
        self.remove_atts_of_type(exclude_type)
        del self.selected_attributes[self.max_number_of_atts:]

    def select_default_object_instances(self):
        self.instances = list(self.object.instances.all())

    def remove_atts_of_type(self, exclude_type):
        self.selected_attributes = list(filter(lambda x: not isinstance(x, exclude_type), self.selected_attributes))

    def get_selected_attribute_labels(self):
        return list(map(lambda x: x.label, self.selected_attributes))

    def get_selected_object_instance_attributes(self):
        instances_with_attributes = []
        for instance in self.instances:
            attribute_values = []
            for att in self.selected_attributes:
                att_inst = instance.get_att_inst(att.label)
                attribute_value = str(att_inst.value) if att_inst else ""
                attribute_values.append(attribute_value)
            instances_with_attributes.append(attribute_values)
        return instances_with_attributes

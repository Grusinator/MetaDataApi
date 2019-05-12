from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from MetaDataApi.metadata.models.instance import BaseAttributeInstance
from MetaDataApi.metadata.models.instance.instance_base import BaseInstance
from MetaDataApi.metadata.models.meta import Attribute
from MetaDataApi.metadata.utils import BuildDjangoSearchArgs
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils


class ObjectInstance(BaseInstance):
    base = models.ForeignKey('Object', on_delete=models.CASCADE, related_name="instances")

    def __str__(self):
        return "Oi:%s.%s" % (self.base.schema.label, self.base.label)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            other = self.build_atts_as_tuple_set_from_inst(other)
        else:
            other = set(other)
        own = self.build_atts_as_tuple_set_from_inst(self)
        return own == other

    @classmethod
    def build_atts_as_tuple_set_from_inst(cls, obj_inst):
        return {(att_inst.base.label, att_inst.value) for att_inst in obj_inst.get_all_attribute_instances()}

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        app_label = 'metadata'
        default_related_name = '%(model_name)s'

    def get_att_inst_with_label(self, label: str) -> BaseAttributeInstance:
        all_atts = self.get_all_att_insts_with_label(label)
        if len(all_atts) != 1:
            raise Exception("att inst: %s did not return 1 but: %s" % (label, len(all_atts)))
        return all_atts[0]

    def get_all_att_insts_with_label(self, label: str) -> list:
        att_base = Attribute.exists_by_label(label, self.base.label)
        if att_base is None:
            raise ObjectDoesNotExist("attribute %s on object %s does not exists" % (label, self.base.label))
        SpecificAttributeInstance = BaseAttributeInstance.get_attribute_instance_from_data_type(att_base.data_type)
        return list(SpecificAttributeInstance.objects.filter(base=att_base, object=self))

    def get_child_obj_instances_with_relation(self, relation_label: str):
        relations = list(self.to_relations.filter(base__label=relation_label))
        return [relation.to_object for relation in relations]

    def get_parrent_obj_instances_with_relation(self, relation_label: str):
        relations = list(self.from_relations.filter(base__label=relation_label))
        return [relation.from_object for relation in relations]

    def create_att_inst(self, att: Attribute, value):
        SpecificAttributeInstance = BaseAttributeInstance.get_attribute_instance_from_data_type(att.data_type)
        att_inst = SpecificAttributeInstance(
            base=Attribute.exists(att),
            object=self,
            value=value
        )
        att_inst.save()

    @classmethod
    def exists(cls, label, children=()):
        arg_builder = BuildDjangoSearchArgs()
        search_args = arg_builder.build_from_json(children)
        search_args["label"] = label
        search_args = BuildDjangoSearchArgs.modify_keys_in_dict(
            search_args, lambda x: "base__" + x)

        return DjangoModelUtils.get_object_or_none(cls, **search_args)

    @classmethod
    def exists_by_parrent_and_attribute_value(cls, parrent_inst_label: str, base_att_label: str):
        raise NotImplementedError()

    def get_related_list(self, include_attributes=False):
        related = []

        builder = BuildDjangoSearchArgs()

        # add "to" relations to current object to list
        # dont match on label but on object
        builder.add_to_obj(self)

        related.extend(list(type(self).objects.filter(**builder.search_args)))

        # clear args
        builder.search_args = {}

        # add "from" relations to current object to list
        # dont match on label but on object
        builder.add_from_obj(self)
        related.extend(list(type(self).objects.filter(**builder.search_args)))

        if include_attributes:
            raise NotImplementedError(
                "include atts has not been implemented yet")
            # TODO add all types of attributes
            # related.append(Attribute.objects.filter(object=self))

        return related

    def get_all_attribute_instances(self):
        attribute_instances = []
        for AttInstance in BaseAttributeInstance.att_inst_to_type_map.keys():
            attribute_instances.extend(AttInstance.objects.filter(object=self))
        return attribute_instances

    # def object_childrens_to_json(self):
    #     raise NotImplementedError

from MetaDataApi.metadata.models import ObjectInstance, Attribute
from MetaDataApi.metadata.rdfs_models.base_rdfs_schema import BaseRdfsSchema
from MetaDataApi.metadata.rdfs_models.descriptors.attributes import *


class DefaultRdfsObjectFactory:
    data_type_to_descriptor_dict = {
        Attribute.DataType.String: StringAttributeDescriptor,
        Attribute.DataType.Boolean: BoolAttributeDescriptor
    }

    @classmethod
    def getObject(cls, object_instance: ObjectInstance):
        attributes = object_instance.base.attributes

        class_attributes = {attribute.label: cls._get_descriptor(attribute) for attribute in attributes}

        # TODO Do the same with relations

        Object = type(object_instance.base.label, (BaseRdfsSchema,), class_attributes)

        object = Object()
        object.object_instance = object_instance
        return object

    @classmethod
    def _get_descriptor(cls, attribute):
        return cls.data_type_to_descriptor_dict.get(attribute.data_type)

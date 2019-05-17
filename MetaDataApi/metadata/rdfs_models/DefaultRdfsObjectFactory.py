from graphql.execution.tests.test_nonnull import DataType

from MetaDataApi.metadata.models import ObjectInstance
from MetaDataApi.metadata.rdfs_models.base_rdfs_model import BaseRdfsModel
from MetaDataApi.metadata.rdfs_models.descriptors.attributes.string_attribute_descriptor import \
    StringAttributeDescriptor


class DefaultRdfsObjectFactory:
    data_type_to_descriptor_dict = {
        DataType.String: StringAttributeDescriptor
    }

    @classmethod
    def getObject(cls, object_instance: ObjectInstance):
        attributes = object_instance.base.attributes

        class_attributes = {attribute.label: cls.get_descriptor(attribute) for attribute in attributes}

        Object = type(object_instance.base.label, (BaseRdfsModel,), class_attributes)

        object = Object()
        object.object_instance = object_instance
        return object

    @classmethod
    def get_descriptor(cls, attribute):
        return cls.data_type_to_descriptor_dict.get(attribute.data_type)

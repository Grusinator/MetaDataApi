from django.urls import reverse

from MetaDataApi.metadata.rdfs_models.base_rdfs_object import BaseRdfsObject
from MetaDataApi.metadata.rdfs_models.descriptors.attributes.string_attribute_descriptor import \
    StringAttributeDescriptor
from MetaDataApi.metadata.rdfs_models.descriptors.relation_descriptor import ObjectRelationDescriptor
from MetaDataApi.metadata.utils.common_utils import StringUtils


class Endpoint(BaseRdfsObject):
    endpoint_name = StringAttributeDescriptor()
    endpoint_url = StringAttributeDescriptor()

    from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_dump import DataDump
    from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import DataProviderO
    has_data_dump = ObjectRelationDescriptor(DataDump, has_many=True)
    data_provider = ObjectRelationDescriptor(DataProviderO, parrent_relation=True)

    def __init__(self, inst_pk: int = None, json_object: dict = None):
        if not inst_pk:
            self.create_self(json_object)
        else:
            super(Endpoint, self).__init__(inst_pk)

    # @property
    # def endpoint_name(self):
    #     return self.get_attribute_value(SI.endpoint_name)
    #
    # @endpoint_name.setter
    # def endpoint_name(self, value):
    #     self.setAttribute(SI.endpoint_name, value)
    #
    # @property
    # def endpoint_url(self):
    #     return self.get_attribute_value(SI.endpoint_url)
    #
    # @endpoint_url.setter
    # def endpoint_url(self, value):
    #     self.setAttribute(SI.endpoint_url, value)
    #
    # @property
    # def data_dumps(self):
    #     data_dumps = self.getChildObjects(SI.has_generated)
    #     return [DataDump(data_dump.pk) for data_dump in data_dumps]
    #
    # @property
    # def data_provider(self):
    #     data_provider = self.getParrentObjects(SI.provider_has_endpoint)[0]
    #     return DataProviderO(data_provider.pk)
    #
    # @property
    # def api_type(self):
    #     return self.get_attribute_value(SI.api_type)

    def get_internal_view_url(self):
        schema = self.data_provider.schema
        return reverse('endpoint_detail', args=[str(schema.label), self.endpoint_name])

    def validate(self):
        valid = not StringUtils.is_string_none(self.endpoint_name) and \
                not StringUtils.is_string_none(self.endpoint_url)
        if not valid:
            raise Exception()

    # TODO fix
    def to_json(self) -> str:
        att_names = ["endpoint_name", "endpoint_url"]
        return self.build_json_from_att_names(att_names)

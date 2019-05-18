from django.urls import reverse

from MetaDataApi.metadata.rdfs_models.base_rdfs_object import BaseRdfsModel
from MetaDataApi.metadata.rdfs_models.descriptors.attributes.string_attribute_descriptor import \
    StringAttributeDescriptor
from MetaDataApi.metadata.rdfs_models.descriptors.relation_descriptor import ObjectRelationDescriptor
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_dump import DataDump
from MetaDataApi.metadata.utils.common_utils import StringUtils


class Endpoint(BaseRdfsModel):
    endpoint_name = StringAttributeDescriptor()
    endpoint_url = StringAttributeDescriptor()
    api_type = StringAttributeDescriptor()
    has_data_dump = ObjectRelationDescriptor(DataDump, has_many=True)
    data_provider_has_endpoint = ObjectRelationDescriptor("DataProviderO", parrent_relation=True)

    def __init__(self, inst_pk: int = None, json_object: dict = None):
        if not inst_pk:
            self.create_self(json_object)
        else:
            super(Endpoint, self).__init__(inst_pk)

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

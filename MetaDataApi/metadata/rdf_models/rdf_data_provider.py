from datetime import datetime

from MetaDataApi.metadata.models import (
    Schema, Object, Attribute,
    ObjectRelation, ObjectInstance,
    StringAttributeInstance)
from MetaDataApi.metadata.rdf_models.base_rdf_model import BaseRdfModel


class RdfDataProvider(BaseRdfModel):
    class SchemaItems:
        schema = Schema(label="meta_data_api")

        data_provider = Object(label="data_provider", schema=schema)

        data_provider_name = Attribute(
            label="data_provider_name",
            object=data_provider,
            data_type=Attribute.DataType.String
        )

        rest_endpoint = Object(label="rest_endpoint", schema=schema)

        endpoint_template_url = Attribute(
            label="endpoint_template_url",
            object=rest_endpoint,
            data_type=Attribute.DataType.String
        )

        endpoint_name = Attribute(
            label="endpoint_name",
            object=rest_endpoint,
            data_type=Attribute.DataType.String
        )

        endpoint_data_dump = Object(label="endpoint_data_dump", schema=schema)

        data_dump_file = Attribute(
            label="data_dump_file",
            object=endpoint_data_dump,
            data_type=Attribute.DataType.File
        )
        date_downloaded = Attribute(
            label="date_downloaded",
            object=endpoint_data_dump,
            data_type=Attribute.DataType.Date
        )
        file_origin_url = Attribute(
            label="file_origin_url",
            object=endpoint_data_dump,
            data_type=Attribute.DataType.String
        )

        has_rest_endpoint = ObjectRelation(
            schema=schema,
            label="has_rest_endpoint",
            from_object=data_provider,
            to_object=rest_endpoint
        )

        has_generated = ObjectRelation(
            schema=schema,
            label="has_generated",
            from_object=rest_endpoint,
            to_object=endpoint_data_dump
        )

    class Endpoint:
        def __init__(self, inst_pk):
            self.endpoint = ObjectInstance.objects.get(pk=inst_pk)

        @property
        def name(self):
            name_att = self.endpoint.get_att_inst(RdfDataProvider.SchemaItems.endpoint_name.label)
            return name_att.value

        @property
        def url(self):
            url_att = self.endpoint.get_att_inst(RdfDataProvider.SchemaItems.endpoint_name.label)
            return url_att.value


    @classmethod
    def create_data_provider(cls, name: str):
        data_provider = cls.create_obj_inst(cls.SchemaItems.data_provider)
        cls.create_att_inst_to_obj_inst(
            data_provider,
            cls.SchemaItems.data_provider_name,
            name
        )
        return data_provider

    @classmethod
    def create_endpoint_to_data_provider(cls, data_provider, endpoint_url: str,
                                         endpoint_name: str):
        rest_endpoint = cls.create_obj_inst(cls.SchemaItems.rest_endpoint)
        cls.create_obj_rel_inst(
            cls.SchemaItems.has_rest_endpoint,
            data_provider,
            rest_endpoint,
        )
        cls.create_att_inst_to_obj_inst(
            rest_endpoint,
            cls.SchemaItems.endpoint_template_url,
            endpoint_url
        )

        cls.create_att_inst_to_obj_inst(
            rest_endpoint,
            cls.SchemaItems.endpoint_name,
            endpoint_name
        )
        return rest_endpoint

    @classmethod
    def create_data_dump(cls, rest_endpoint: ObjectInstance,
                         file, date: datetime = datetime.now()):
        endpoint_data_dump = cls.create_obj_inst(
            Object.exists(cls.SchemaItems.endpoint_data_dump)
        )
        cls.create_obj_rel_inst(
            obj_rel=cls.SchemaItems.has_generated,
            from_object=rest_endpoint,
            to_object=endpoint_data_dump
        )
        cls.create_att_inst_to_obj_inst(
            endpoint_data_dump,
            cls.SchemaItems.date_downloaded,
            value=date
        )
        cls.create_att_inst_to_obj_inst(
            endpoint_data_dump,
            cls.SchemaItems.data_dump_file,
            value=file
        )
        return endpoint_data_dump

    @classmethod
    def get_endpoint(cls, provider: ObjectInstance, rest_endpoint_name: str):
        endpoints = cls.get_all_endpoints(provider)
        return cls.find_endpoint_with_name(endpoints, rest_endpoint_name)

    @classmethod
    def get_all_endpoints_as_objects(cls, provider: ObjectInstance):
        endpoints = cls.get_all_endpoints(provider)
        return [cls.Endpoint(endpoint.pk) for endpoint in endpoints]

    @classmethod
    def find_endpoint_with_name(cls, endpoints: list, rest_endpoint_name: str) -> ObjectInstance:
        for endpoint in endpoints:
            name = StringAttributeInstance.objects.filter(
                object=endpoint,
                base=Attribute.exists(cls.SchemaItems.endpoint_name),
                value=rest_endpoint_name
            ).first()
            if name:
                return endpoint

    @classmethod
    def get_all_endpoints(cls, provider: ObjectInstance) -> list:
        search_args = {
            "from_relations__from_object": provider
        }
        return list(ObjectInstance.objects.filter(**search_args))

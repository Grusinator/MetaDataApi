from datetime import datetime

from MetaDataApi.metadata.models import (
    Schema, Object, Attribute,
    ObjectRelation, ObjectInstance,
    StringAttributeInstance)
from MetaDataApi.metadata.rdfs_models.base_rdfs_model import BaseRdfsModel
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.rdf_model_not_correctly_initialized_exception import \
    RdfModelNotCorrectlyInitializedException


class RdfsDataProvider(BaseRdfsModel):
    class SchemaItems:

        schema = Schema(label="meta_data_api")

        data_provider = Object(label="data_provider", schema=schema)

        data_provider_name = Attribute(
            label="data_provider_name",
            object=data_provider,
            data_type=Attribute.DataType.String
        )

        scope = Attribute(
            label="scope",
            object=data_provider,
            data_type=Attribute.DataType.String
        )

        api_type = Attribute(
            label="api_type",
            object=data_provider,
            data_type=Attribute.DataType.String
        )

        authorize_url = Attribute(
            label="authorize_url",
            object=data_provider,
            data_type=Attribute.DataType.String
        )
        access_token_url = Attribute(
            label="access_token_url",
            object=data_provider,
            data_type=Attribute.DataType.String
        )
        api_endpoint = Attribute(
            label="api_endpoint",
            object=data_provider,
            data_type=Attribute.DataType.String
        )

        endpoint = Object(label="endpoint", schema=schema)

        endpoint_url = Attribute(
            label="endpoint_url",
            object=endpoint,
            data_type=Attribute.DataType.String
        )

        endpoint_name = Attribute(
            label="endpoint_name",
            object=endpoint,
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
            data_type=Attribute.DataType.DateTime
        )
        file_origin_url = Attribute(
            label="file_origin_url",
            object=endpoint_data_dump,
            data_type=Attribute.DataType.String
        )

        loaded = Attribute(
            label="loaded",
            object=endpoint_data_dump,
            data_type=Attribute.DataType.Boolean
        )

        provider_has_endpoint = ObjectRelation(
            schema=schema,
            label="provider_has_endpoint",
            from_object=data_provider,
            to_object=endpoint
        )

        has_generated = ObjectRelation(
            schema=schema,
            label="has_generated",
            from_object=endpoint,
            to_object=endpoint_data_dump
        )

    @classmethod
    def create_data_provider(cls, name: str):
        if not cls.do_schema_items_exists():
            raise RdfModelNotCorrectlyInitializedException()

        data_provider = cls.create_obj_inst(cls.SchemaItems.data_provider)
        cls.create_att_inst_to_obj_inst(
            data_provider,
            cls.SchemaItems.data_provider_name,
            name
        )
        return data_provider

    @classmethod
    def create_endpoint_to_data_provider(cls, data_provider, endpoint_name: str, endpoint_url: str):
        rest_endpoint = cls.create_obj_inst(cls.SchemaItems.endpoint)
        cls.create_obj_rel_inst(
            cls.SchemaItems.provider_has_endpoint,
            data_provider,
            rest_endpoint,
        )
        cls.create_att_inst_to_obj_inst(
            rest_endpoint,
            cls.SchemaItems.endpoint_url,
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

        cls.create_att_inst_to_obj_inst(
            endpoint_data_dump,
            cls.SchemaItems.loaded,
            value=False
        )
        return endpoint_data_dump

    @classmethod
    def get_endpoint(cls, provider: ObjectInstance, rest_endpoint_name: str):
        endpoints = cls.get_all_endpoints(provider)
        return cls.find_endpoint_with_name(endpoints, rest_endpoint_name)

    @classmethod
    def get_all_endpoints(cls, provider: ObjectInstance) -> list:
        search_args = {
            "from_relations__from_object": provider,
            "base": Object.exists(RdfsDataProvider.SchemaItems.endpoint)
        }
        return list(ObjectInstance.objects.filter(**search_args))

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
    def get_all_data_dumps(cls, endpoint):
        search_args = {
            "from_relations__from_object": endpoint,
            "base": Object.exists(RdfsDataProvider.SchemaItems.endpoint_data_dump)
        }
        return list(ObjectInstance.objects.filter(**search_args))

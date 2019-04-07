from datetime import datetime

from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation
from MetaDataApi.metadata.rdf_models.base_rdf_model import BaseRdfModel


class RdfDataProviders(BaseRdfModel):
    class SchemaItems:
        schema = Schema(label="meta_data_api")
        rest_endpoint = Object(label="rest_endpoint", schema=schema)

        endpoint_data_dump = Object(label="endpoint_data_dump", schema=schema)

        data_dump_file = Attribute(
            label="data_dump_file",
            object=endpoint_data_dump,
            data_type="file"
        )
        date_downloaded = Attribute(
            label="date_downloaded",
            object=endpoint_data_dump,
            data_type="date"
        )
        endpoint_url = Attribute(
            label="endpoint_url",
            object=endpoint_data_dump,
            data_type="string"
        )

        has_generated = ObjectRelation(
            schema=schema,
            label="has_generated",
            from_object=rest_endpoint,
            to_object=endpoint_data_dump
        )

    @classmethod
    def _get_schema(cls) -> Schema:
        return cls.SchemaItems.schema

    @classmethod
    def _get_attributes(cls):
        return [
            cls.SchemaItems.data_dump_file,
            cls.SchemaItems.date_downloaded,
            cls.SchemaItems.endpoint_url
        ]

    @classmethod
    def _get_objects(cls):
        return [
            cls.SchemaItems.rest_endpoint,
            cls.SchemaItems.endpoint_data_dump
        ]

    @classmethod
    def _get_object_relations(cls):
        return [
            cls.SchemaItems.has_generated
        ]

    @classmethod
    def create_data_provider(cls):
        rest_endpoint = cls.create_obj_inst(cls.SchemaItems.rest_endpoint)
        return rest_endpoint

    def delete_data_provider(self):
        pass

    @classmethod
    def create_data_dump(cls, provider, date: datetime, file):
        endpoint_data_dump = cls.create_obj_inst(
            cls.SchemaItems.endpoint_data_dump
        )
        cls.create_obj_rel_inst(
            obj_rel=cls.SchemaItems.has_generated,
            from_object=provider,
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

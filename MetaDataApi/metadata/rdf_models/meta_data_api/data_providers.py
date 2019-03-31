from datetime import datetime
from enum import Enum

from MetaDataApi.metadata.rdf_models.base_rdf_model import BaseRdfModel


class RdfDataProviders(BaseRdfModel):
    schema_label = "meta_data_api"

    class ObjectLabels(Enum):
        rest_endpoint = "rest_endpoint"
        endpoint_data_dump = "endpoint_data_dump"

    class ObjectRelationLabels(Enum):
        has_generated = "has_generated"

    class AttributeLabels(Enum):
        data_dump_file = "data_dump_file"
        date_downloaded = "date_downloaded"
        endpoint_url = "endpoint_url"

    @classmethod
    def create_data_provider(cls):
        rest_endpoint = cls.create_obj_inst(cls.ObjectLabels.rest_endpoint)
        return rest_endpoint

    def delete_data_provider(self):
        pass

    @classmethod
    def create_data_dump(cls, provider, date: datetime, file):
        endpoint_data_dump = cls.create_obj_inst(
            cls.ObjectLabels.endpoint_data_dump
        )
        cls.create_obj_rel_inst(
            rel_label=cls.ObjectRelationLabels.has_generated,
            from_object=provider,
            to_object=endpoint_data_dump
        )

        cls.create_att_inst_to_obj_inst(
            endpoint_data_dump,
            cls.AttributeLabels.date_downloaded,
            value=date
        )

        cls.create_att_inst_to_obj_inst(
            endpoint_data_dump,
            cls.AttributeLabels.data_dump_file,
            value=file
        )

        return endpoint_data_dump

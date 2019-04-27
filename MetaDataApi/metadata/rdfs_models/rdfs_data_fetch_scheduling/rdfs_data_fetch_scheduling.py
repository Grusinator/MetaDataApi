from MetaDataApi.metadata.models import (
    Schema, Object, Attribute,
    ObjectRelation)
from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
from MetaDataApi.metadata.rdfs_models.base_rdfs_model import BaseRdfModel


class RdfsDataFetchScheduling(BaseRdfModel):
    class SchemaItems:
        schema = Schema(label="meta_data_api")

        data_fetch_schedule = Object(label="data_fetch_schedule", schema=schema)

        has_data_fetch_schedule = ObjectRelation(
            schema=schema,
            label="has_data_fetch_schedule",
            from_object=RdfsDataProvider.SchemaItems.endpoint,
            to_object=data_fetch_schedule
        )
        time_interval = Attribute(
            label="data_provider_name",
            object=data_fetch_schedule,
            data_type=Attribute.DataType.String
        )

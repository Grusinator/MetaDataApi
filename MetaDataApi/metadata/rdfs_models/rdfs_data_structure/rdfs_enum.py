from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation
from MetaDataApi.metadata.rdfs_models.base_rdfs_schema import BaseRdfsSchema


class RdfsEnum(BaseRdfsSchema):
    class SchemaItems:
        schema = Schema(label="meta_data_api")

        enum = Object(label="enum", schema=schema)

        enum_name = Attribute(
            label="enum_name",
            object=enum,
            data_type=Attribute.DataType.String
        )

        enum_element = Object(label="enum_element", schema=schema)

        enum_element_name = Attribute(
            label="enum_element_name",
            object=enum_element,
            data_type=Attribute.DataType.String
        )

        rest_endpoint = Object(label="rest_endpoint", schema=schema)

        has_enum_element = ObjectRelation(
            schema=schema,
            label="has_enum_element",
            from_object=enum,
            to_object=enum_element
        )

        # this is an abstract object that can be inherrited from
        enum_type_object = Object(label="enum_type_object", schema=schema)

        enum_enforces_choices = ObjectRelation(
            schema=schema,
            label="enum_enforces_choices",
            from_object=enum,
            to_object=enum_type_object
        )

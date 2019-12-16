from metadata.models import StringAttribute, Node, SchemaNode, Schema


class InstanceMocks:

    @staticmethod
    def ObjectInstance1():
        schema = Schema.create_new_empty_schema("meta_data_api")
        obj = SchemaNode(label="dummy", schema=schema)
        return Node(
            base=obj
        )

    @staticmethod
    def MockStringAttributeInstance():
        return StringAttribute(
            value="somevalue",
            obj=InstanceMocks.ObjectInstance1()
        )

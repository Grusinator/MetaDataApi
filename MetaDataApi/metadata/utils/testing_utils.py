from MetaDataApi.metadata.models import Schema, SchemaEdge, SchemaNode, BaseAttribute


class TestingUtils:

    @classmethod
    def get_all_items_from_schema(cls, schema_label):
        schema = Schema.exists_by_label(schema_label)
        objects = list(schema.schema_nodes.all())
        attributes = []
        [attributes.extend(obj.attributes.all()) for obj in objects]
        schema_edges = list(schema.schema_edges.all())
        return [schema] + objects + attributes + schema_edges

    @classmethod
    def get_all_item_labels_from_schema(cls, schema_label):
        labels = list(map(lambda x: x.label, cls.get_all_items_from_schema(schema_label)))
        labels.sort()
        return labels

    @classmethod
    def get_all_object_instances_from_schema(cls, schema_label):
        metas = cls.get_all_items_from_schema(schema_label)
        metas.remove(Schema.exists_by_label(schema_label))
        instances = []
        for meta in metas:
            if isinstance(meta, (SchemaNode, SchemaEdge)):
                instances.extend(meta.instances.all())
            else:
                instances.extend(BaseAttribute.get_all_instances_from_base(meta))
        return instances

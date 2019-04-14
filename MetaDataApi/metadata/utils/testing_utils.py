from MetaDataApi.metadata.models import Schema, ObjectRelation, Object


class TestingUtils:

    @classmethod
    def get_all_items_from_schema(cls, schema_label):
        schema = Schema.exists_by_label(schema_label)
        objects = list(schema.object_list.all())
        attributes = []
        [attributes.extend(obj.attributes.all()) for obj in objects]
        object_relations = list(schema.object_relations.all())
        return [schema] + objects + attributes + object_relations

    @classmethod
    def get_all_item_labels_from_schema(cls, schema_label):
        return list(map(
            lambda x: x.label,
            cls.get_all_items_from_schema(schema_label)
        ))

    @classmethod
    def get_all_object_instances_from_schema(cls, schema_label):
        metas = cls.get_all_items_from_schema(schema_label)
        metas.remove(Schema.exists_by_label(schema_label))
        instances = []
        for meta in metas:
            if isinstance(meta, (Object, ObjectRelation)):
                instances.extend(meta.instances.all())
            else:
                instances.extend(meta.all_instances)
        return instances

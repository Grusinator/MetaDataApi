from django.db import models

from MetaDataApi.metadata.models.meta import BaseMeta


class ObjectRelation(BaseMeta):
    schema = models.ForeignKey(
        'Schema', related_name='object_relations', on_delete=models.CASCADE)
    from_object = models.ForeignKey(
        'Object', related_name='to_relations', on_delete=models.CASCADE)
    to_object = models.ForeignKey(
        'Object', related_name='from_relations', on_delete=models.CASCADE)

    def __str__(self):
        return "R:%s - %s - %s" % (
            self.from_object.label,
            self.label,
            self.to_object.label)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    @classmethod
    def exists(cls, label: str, from_object__label: str,
               to_object__label: str, schema__label: str):
        search_args = dict(locals())
        search_args.pop("cls")

        return cls.get_schema_item(cls, **search_args)

    @classmethod
    def exists_obj_rel(cls, obj_rel):
        return cls.exists(
            obj_rel.label,
            obj_rel.from_object.label,
            obj_rel.to_object.label,
            obj_rel.schema.label
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        unique_together = ('label', 'schema', "from_object", "to_object")
        app_label = 'metadata'

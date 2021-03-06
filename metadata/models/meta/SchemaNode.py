from django.db import models
from django.urls import reverse

from MetaDataApi.utils import BuildDjangoSearchArgs
from metadata.models.meta.BaseMeta import BaseMeta


class SchemaNode(BaseMeta):
    # related name should not be objects, because that will cause problems
    schema = models.ForeignKey(
        'Schema', related_name='schema_nodes', on_delete=models.CASCADE)

    def __str__(self):
        return "O:%s.%s" % (self.schema.label, self.label)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            # return self.__dict__ == other.__dict__

            def inner_join_by_label(from1, from2):
                from1 = [elm.label for elm in from1]
                from2 = [elm.label for elm in from2]

                commons = list(set(from1) & set(from2))
                return any(commons)

            sel_f = hasattr(self, "from_objects")
            oth_f = hasattr(other, "from_objects")

            if sel_f and oth_f:
                from_obj_match = inner_join_by_label(
                    self.from_objects,
                    other.from_objects)
            else:
                # if they are not equal
                from_obj_match = sel_f == oth_f

            return self.schema == other.schema and \
                   self.label == other.label and \
                   from_obj_match

        else:
            return False

    def get_related_list(self, include_attributes=True):
        related = []

        builder = BuildDjangoSearchArgs()

        # add "to" relations to current object to list
        # dont match on label but on object
        builder.add_to_obj(self)
        related.extend(list(type(self).objects.filter(**builder.search_args)))

        # clear args
        builder.search_args = {}

        # add "from" relations to current object to list
        # dont match on label but on object
        builder.add_from_obj(self)
        related.extend(list(type(self).objects.filter(**builder.search_args)))

        # TODO refactor this out in own service, so that imports are not getting circular
        # if include_attributes:
        #     related.extend(list(SchemaAttribute.objects.filter(object=self)))

        return related

    @classmethod
    def exists_by_label(cls, label: str, schema__label: str, raise_error: bool = False):
        search_args = dict(locals())
        search_args.pop("cls")
        search_args.pop("raise_error")
        return cls.get_schema_item(cls, raise_error=raise_error, **search_args)

    @classmethod
    def exists(cls, obj):
        return cls.exists_by_label(obj.label, obj.schema.label)

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_internal_view_url(self):
        schema = self.schema
        return reverse('objects', args=[str(schema.label), self.label])

    class Meta:
        unique_together = ('label', 'schema')
        app_label = 'metadata'

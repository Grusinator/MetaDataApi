from django.db import models
from MetaDataApi.metadata.custom_storages import MediaStorage
from datetime import datetime
from MetaDataApi.metadata.utils.django_model_utils import BuildDjangoSearchArgs, DjangoModelUtils
from MetaDataApi.metadata.utils.common_utils import DictUtils
# Create your models here.


class BaseMeta(models.Model):
    label = models.TextField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class Schema(models.Model):
    label = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    rdfs_file = models.FileField(
        upload_to="schemas",
        null=True, blank=True, storage=MediaStorage())

    def __str__(self):
        return "S:" + self.label

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.url == other.url and \
                self.label == other.label
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        app_label = 'metadata'


class Object(BaseMeta):
    # related name should not be objects, because that will cause problems
    schema = models.ForeignKey(
        Schema, related_name='object_list', on_delete=models.CASCADE)

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

        if include_attributes:
            related.extend(list(Attribute.objects.filter(object=self)))

        return related

    @classmethod
    def exists(cls, label: str, schema__label: str):
        search_args = dict(locals())
        search_args.pop("cls")
        return DjangoModelUtils.get_object_or_none(cls, **search_args)

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        unique_together = ('label', 'schema')
        app_label = 'metadata'


class Attribute(BaseMeta):
    data_type_map = {
        datetime: "datetime",
        float: "float",
        int: "int",
        bool: "bool",
        str: "string",
        type(None): "unknown"
    }
    data_type_choises = [(x, x) for x in data_type_map.values()]

    # db Fields
    data_type = models.TextField(choices=data_type_choises)
    data_unit = models.TextField()
    object = models.ForeignKey(
        Object, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return "A:%s.%s" % (self.object.label, self.label)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    @classmethod
    def exists(cls, label: str, object__label: str):
        search_args = dict(locals())
        search_args.pop("cls")
        return DjangoModelUtils.get_object_or_none(cls, **search_args)

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def assert_data_type(cls, attribute, data_type):
        data_type_name = cls.data_type_map[data_type]
        assert attribute.data_type == data_type_name, \
            "the found attr: %s has type %s, but it must be a %s" % (
                attribute.label,
                attribute.data_type,
                str(data_type_name)
            )

    class Meta:
        unique_together = ('label', 'object')
        app_label = 'metadata'


class ObjectRelation(BaseMeta):
    schema = models.ForeignKey(
        Schema, related_name='object_relations', on_delete=models.CASCADE)
    from_object = models.ForeignKey(
        Object, related_name='to_relations', on_delete=models.CASCADE)
    to_object = models.ForeignKey(
        Object, related_name='from_relations', on_delete=models.CASCADE)

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

        return DjangoModelUtils.get_object_or_none(cls, **search_args)

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        unique_together = ('label', 'schema', "from_object", "to_object")
        app_label = 'metadata'


class UnmappedObject(BaseMeta):
    parrent_label = models.TextField()
    childrens = models.TextField()

    class Meta:
        app_label = 'metadata'

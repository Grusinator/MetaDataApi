from django.db import models
from MetaDataApi.metadata.custom_storages import MediaStorage
from datetime import datetime
# Create your models here.


class Schema(models.Model):

    label = models.TextField()
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


class Object(models.Model):
    label = models.TextField()
    description = models.TextField(null=True, blank=True)
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

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        app_label = 'metadata'


class Attribute(models.Model):
    data_type_map = {
        datetime: "datetime",
        float: "float",
        int: "int",
        bool: "bool",
        str: "string",
        None: "unknown"
    }
    data_type_choises = [(x, x) for x in data_type_map.values()]

    label = models.TextField()
    description = models.TextField(null=True, blank=True)
    datatype = models.TextField(choices=data_type_choises)
    dataunit = models.TextField()
    object = models.ForeignKey(
        Object, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return "A:%s.%s" % (self.object.label, self.label)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        app_label = 'metadata'


class ObjectRelation(models.Model):
    label = models.TextField()
    description = models.TextField(null=True, blank=True)
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

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        app_label = 'metadata'


class UnmappedObject(models.Model):
    label = models.TextField()
    parrent_label = models.TextField()
    childrens = models.TextField()

    class Meta:
        app_label = 'metadata'

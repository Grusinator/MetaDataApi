from django.db import models
from .custom_storages import MediaStorage

# Create your models here.


class Schema(models.Model):

    label = models.TextField()
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    rdf_file = models.FileField(
        upload_to="schemas",
        null=True, blank=True, storage=MediaStorage())

    def __str__(self):
        return "S:" + self.label

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

    class Meta:
        app_label = 'metadata'


class Attribute(models.Model):
    label = models.TextField()
    description = models.TextField(null=True, blank=True)
    datatype = models.TextField()
    dataunit = models.TextField()
    object = models.ForeignKey(
        Object, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return "A:%s.%s" % (self.object.label, self.label)

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

    class Meta:
        app_label = 'metadata'


# instance classes

class ObjectInstance(models.Model):
    base = models.ForeignKey(
        Object,
        related_name='object_instances', on_delete=models.CASCADE)

    def __str__(self):
        return "O:%s.%s" % (self.base.schema.label, self.base.label)


class ObjectRelationInstance(models.Model):
    base = models.ForeignKey(
        ObjectRelation,
        related_name='object_relation_instances', on_delete=models.CASCADE)
    from_object = models.ForeignKey(
        ObjectInstance,
        related_name='to_relations', on_delete=models.CASCADE)
    to_object = models.ForeignKey(
        ObjectInstance,
        related_name='from_relations', on_delete=models.CASCADE)

    def __str__(self):
        return "R:%s - %s - %s" % (
            self.base.from_object.label,
            self.base.label,
            self.base.to_object.label)


class AttributeInstance(models.Model):
    base = models.ForeignKey(
        Attribute,
        related_name='attribute_instances', on_delete=models.CASCADE)
    value = models.TextField()
    object = models.ForeignKey(
        ObjectInstance, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return "A:%s.%s:%s" % (self.base.object.label, self.base.label, self.value)

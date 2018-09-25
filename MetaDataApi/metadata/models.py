from django.db import models

# Create your models here.


class Schema(models.Model):

    label = models.TextField()
    description = models.TextField()
    url = models.URLField(unique=True)

    def __str__(self):
        return self.label

    class Meta:
        app_label = 'metadata'


class Object(models.Model):
    label = models.TextField()
    description = models.TextField()
    # related name should not be objects, because that will cause problems
    schema = models.ForeignKey(
        Schema, related_name='object_list', on_delete=models.CASCADE)

    def __str__(self):
        return "%s.%s" % (self.schema.label, self.label)

    class Meta:
        app_label = 'metadata'


class Attribute(models.Model):
    label = models.TextField()
    description = models.TextField()
    datatype = models.TextField()
    object = models.ForeignKey(
        Object, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return "%s.%s" % (self.object.label, self.label)

    class Meta:
        app_label = 'metadata'


class ObjectRelation(models.Model):
    label = models.TextField()
    url = models.TextField()
    from_object = models.ForeignKey(
        Object, related_name='to_relations', on_delete=models.CASCADE)
    to_object = models.ForeignKey(
        Object, related_name='from_relations', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s" % (
            self.to_object.label,
            self.label,
            self.from_object.label)

    class Meta:
        app_label = 'metadata'

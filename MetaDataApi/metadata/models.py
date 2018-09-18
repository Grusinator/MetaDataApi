from django.db import models

# Create your models here.

class Schema(models.Model):
    #source category and label should be unique
    name = models.TextField()
    description = models.TextField()
    origin = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'metadata'

class Object(models.Model):
    #source category and label should be unique
    name = models.TextField()
    description = models.TextField()
    schema = models.ForeignKey(Schema, related_name='objects', on_delete=models.CASCADE) 

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'metadata'
        
class Attribute(models.Model):
    #source category and label should be unique
    name = models.TextField()
    datatype = models.TextField()
    object = models.ForeignKey(Object, related_name='attributes', on_delete=models.CASCADE) 

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'metadata'

class ObjectRelation(models.Model):
    name = models.TextField()
    from_object = models.OneToOneField(Object, related_name='to_relations', on_delete=models.CASCADE) 
    to_object = models.OneToOneField(Object, related_name='from_relations', on_delete=models.CASCADE) 
    def __str__(self):
        return self.name

    class Meta:
        app_label = 'metadata'

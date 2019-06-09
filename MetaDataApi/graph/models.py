from django.db import models


from dynamic_models.models import AbstractModelSchema, AbstractFieldSchema


class ModelSchema(AbstractModelSchema):
    pass


class FieldSchema(AbstractFieldSchema):
    pass


class Dummy(models.Model):
    value = models.IntegerField()

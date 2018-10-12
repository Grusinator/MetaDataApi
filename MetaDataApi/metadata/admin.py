from django.contrib import admin

# Register your models here.
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation,
    ObjectInstance, ObjectRelationInstance,
    AttributeInstance)

list = [Schema, Object, Attribute, ObjectRelation,
        ObjectInstance, ObjectRelationInstance,
        AttributeInstance]

[admin.site.register(model) for model in list]

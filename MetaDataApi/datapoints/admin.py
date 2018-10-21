from django.contrib import admin

# Register your models here.
from MetaDataApi.datapoints.models import (
    RawData,
    ObjectInstance,
    ObjectRelationInstance,
    GenericAttributeInstance,
    FloatAttributeInstance,
    StringAttributeInstance)

models = (
    RawData,
    ObjectInstance,
    ObjectRelationInstance,
    GenericAttributeInstance,
    FloatAttributeInstance,
    StringAttributeInstance)

[admin.site.register(model) for model in models]

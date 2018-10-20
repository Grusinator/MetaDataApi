from django.contrib import admin

# Register your models here.
from MetaDataApi.datapoints.models import (
    RawData,
    ObjectInstance,
    ObjectRelationInstance,
    GenericAttributeInstance,
    TemporalFloatAttributeInstance,
    TemporalStringAttributeInstance)

models = (
    RawData,
    ObjectInstance,
    ObjectRelationInstance,
    GenericAttributeInstance,
    TemporalFloatAttributeInstance,
    TemporalStringAttributeInstance)

[admin.site.register(model) for model in models]

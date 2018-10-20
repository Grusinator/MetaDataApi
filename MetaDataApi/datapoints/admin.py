from django.contrib import admin

# Register your models here.
from MetaDataApi.datapoints.models import (
    DatapointV2, MetaData, RawData,
    ObjectInstance,
    ObjectRelationInstance,
    GenericAttributeInstance,
    TemporalFloatAttributeInstance,
    TemporalStringAttributeInstance)

models = (
    DatapointV2, MetaData, RawData,
    ObjectInstance,
    ObjectRelationInstance,
    GenericAttributeInstance,
    TemporalFloatAttributeInstance,
    TemporalStringAttributeInstance)

[admin.site.register(model) for model in models]

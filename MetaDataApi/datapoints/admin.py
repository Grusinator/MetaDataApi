from django.contrib import admin

# Register your models here.
from MetaDataApi.datapoints.models import *

models = (
    RawData,
    ObjectInstance,
    ObjectRelationInstance,
    FloatAttributeInstance,
    StringAttributeInstance,
    IntAttributeInstance,
    BoolAttributeInstance,
    ImageAttributeInstance)

[admin.site.register(model) for model in models]

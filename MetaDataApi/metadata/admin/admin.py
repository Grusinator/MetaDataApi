from django.contrib import admin

# Register your models here.
from MetaDataApi.metadata.models import *

models = (
    # meta
    Object, Attribute, ObjectRelation,
    # instances
    RawData,
    ObjectInstance,
    ObjectRelationInstance)

[admin.site.register(model) for model in models]

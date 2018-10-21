from django.contrib import admin

# Register your models here.
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

models = (Schema, Object, Attribute, ObjectRelation)

[admin.site.register(model) for model in models]

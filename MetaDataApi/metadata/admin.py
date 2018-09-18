from django.contrib import admin

# Register your models here.
from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation

list = [Schema, Object, Attribute, ObjectRelation]

for model in list:
    admin.site.register(model)
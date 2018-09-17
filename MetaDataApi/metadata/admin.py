from django.contrib import admin

# Register your models here.
from MetaDataApi.metadata.models import Schema, Object, Attribute

list = [Schema, Object, Attribute]
for model in list:
    admin.site.register(model)
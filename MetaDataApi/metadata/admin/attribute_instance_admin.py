from django.contrib import admin

# Register your models here.
from MetaDataApi.metadata.models import *

models = (
    # meta
    FloatAttributeInstance,
    StringAttributeInstance,
    IntAttributeInstance,
    BoolAttributeInstance,
    ImageAttributeInstance,
    FileAttributeInstance,
)


class BaseAttributeInstanceAdmin(admin.ModelAdmin):
    list_display = ['value', 'base', "object"]
    ordering = ['value', 'base', "object"]


for model in models:
    AttributeInstanceAdmin = type(model.__name__ + "Admin",
                                  (BaseAttributeInstanceAdmin,), {})

    admin.site.register(model, AttributeInstanceAdmin)

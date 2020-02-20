from django.contrib import admin

from .models.dynamic_meta_object import DynamicMetaObject


# admin.site.register(Dummy)

@admin.register(DynamicMetaObject)
class DynamicMetaObjectAdmin(admin.ModelAdmin):
    list_display = ['dynamic_model', 'data_provider']
    ordering = ['data_provider']

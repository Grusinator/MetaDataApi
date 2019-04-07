from django.contrib import admin

from MetaDataApi.metadata.models import Attribute


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['object', 'label', 'data_type', 'description']
    ordering = ['object', 'label', 'data_type']
    actions = []


admin.site.register(Attribute, AttributeAdmin)

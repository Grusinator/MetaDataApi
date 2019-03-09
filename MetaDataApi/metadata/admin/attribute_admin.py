from django.contrib import admin

from metadata.models import Attribute


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['object', 'label', 'data_type', 'data_unit', 'description']
    ordering = ['object', 'label', 'data_type', 'data_unit']
    actions = []


admin.site.register(Attribute, AttributeAdmin)

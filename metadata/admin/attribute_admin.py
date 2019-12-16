from django.contrib import admin

from metadata.models import SchemaAttribute


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['object', 'label', 'data_type', 'description']
    ordering = ['object', 'label', 'data_type']
    actions = []


admin.site.register(SchemaAttribute, AttributeAdmin)

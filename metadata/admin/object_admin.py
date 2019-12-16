from django.contrib import admin

from metadata.models import SchemaNode


class ObjectAdmin(admin.ModelAdmin):
    list_display = ['schema', 'label', 'description']
    ordering = ['label', 'schema']
    actions = []


admin.site.register(SchemaNode, ObjectAdmin)

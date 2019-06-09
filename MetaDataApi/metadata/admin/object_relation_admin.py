from django.contrib import admin

from MetaDataApi.metadata.models import SchemaEdge


class ObjectRelationAdmin(admin.ModelAdmin):
    list_display = ['schema', 'label', "from_object", "to_object", 'description']
    ordering = ['schema', 'label', "from_object", "to_object"]
    actions = []


admin.site.register(SchemaEdge, ObjectRelationAdmin)

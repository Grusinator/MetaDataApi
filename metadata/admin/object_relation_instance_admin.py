from django.contrib import admin

from metadata.models import Edge


class ObjectRelationAdmin(admin.ModelAdmin):
    list_display = ['owner', 'base', "from_object", "to_object"]
    ordering = ['owner', 'base', "from_object", "to_object"]
    actions = []


admin.site.register(Edge, ObjectRelationAdmin)

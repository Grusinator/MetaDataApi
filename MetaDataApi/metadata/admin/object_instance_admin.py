from django.contrib import admin

from MetaDataApi.metadata.models import ObjectInstance


class ObjectInstanceAdmin(admin.ModelAdmin):
    list_display = ['owner', 'base']
    ordering = ['owner', 'base']
    actions = []


admin.site.register(ObjectInstance, ObjectInstanceAdmin)

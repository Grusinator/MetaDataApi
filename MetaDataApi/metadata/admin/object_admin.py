from django.contrib import admin

from MetaDataApi.metadata.models import Object


class ObjectAdmin(admin.ModelAdmin):
    list_display = ['schema', 'label', 'description']
    ordering = ['label', 'schema']
    actions = []


admin.site.register(Object, ObjectAdmin)

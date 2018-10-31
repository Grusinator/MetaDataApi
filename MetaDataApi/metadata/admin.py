from django.contrib import admin
import webbrowser

# Register your models here.
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

from MetaDataApi.metadata.services import ExportSchemaService,
AddRdfSchemaService

models = (Object, Attribute, ObjectRelation)


[admin.site.register(model) for model in models]


def add_rdf_defaults(modeladmin, request, queryset):
    AddRdfSchemaService.execute({
        "url": "baseschema"
    })


def visualize(modeladmin, request, queryset):
    for schema in queryset:
        webbrowser.open_new_tab(
            "http://visualdataweb.de/webvowl/#iri=" + schema.url)


def export_schema(modeladmin, request, queryset):

    for schema in queryset:
        ExportSchemaService.execute({
            "schema_label": schema.label,
        })


export_schema.short_description = "Export to RDF file (use the url)"


class SchemaAdmin(admin.ModelAdmin):
    list_display = ['label', 'url']
    ordering = ['label']
    actions = [export_schema, visualize]


admin.site.register(Schema, SchemaAdmin)

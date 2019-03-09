import webbrowser

from django.contrib import admin

from MetaDataApi.metadata.models import Schema
from MetaDataApi.metadata.services import (
    ExportSchemaService, AddRdfSchemaService, AddJsonSchemaService)


def relate_to_foaf(modeladmin, request, queryset):
    pass


def add_open_m_health(modeladmin, request, queryset):
    AddJsonSchemaService.execute({
        "url": "open_m_health"
    })


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
    actions = [export_schema, visualize, add_open_m_health, add_rdf_defaults]


admin.site.register(Schema, SchemaAdmin)

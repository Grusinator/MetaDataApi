import django

django.setup()

from MetaDataApi.metadata.services.rdf import rdfService
from MetaDataApi.metadata.models import Schema, Object, ObjectRelation


def update_base_schema():

    service = rdfService()

    service.create_default_schemas()

    schema_list = Schema.objects.first()

    a = 1


update_base_schema()

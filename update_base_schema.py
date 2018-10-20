import django

django.setup()

from MetaDataApi.metadata.services.rdf import RdfService
from MetaDataApi.metadata.models import Schema, Object, ObjectRelation


def update_base_schema():

    service = RdfService()

    service.write_to_db_baseschema()

    schema_list = Schema.objects.first()

    a = 1


update_base_schema()

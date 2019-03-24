import django

from MetaDataApi.metadata.models import Schema
from MetaDataApi.metadata.services.all_services.rdf_schema_service import RdfSchemaService

django.setup()


def update_base_schema():

    service = RdfSchemaService()

    service.write_to_db_baseschema()

    schema_list = Schema.objects.first()

    a = 1


update_base_schema()

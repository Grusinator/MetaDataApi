from MetaDataApi.metadata.models import Schema, Object, ObjectRelation
from MetaDataApi.metadata.services.rdf import RdfSchemaService
import django

django.setup()


def update_base_schema():

    service = RdfSchemaService()

    service.write_to_db_baseschema()

    schema_list = Schema.objects.first()

    a = 1


update_base_schema()

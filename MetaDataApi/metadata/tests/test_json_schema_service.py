import django
from django.test import TestCase, TransactionTestCase


# TODO: Configure your database in settings.py and sync before running tests.


class TestJsonService(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()
        super(TestJsonService, cls).setUpClass()

        # populate the database
        from MetaDataApi.metadata.services import RdfSchemaService
        from MetaDataApi.metadata.services import (
            JsonSchemaService
        )
        rdf_service = RdfSchemaService()

        rdf_service.write_to_db_baseschema()

        service = JsonSchemaService()
        # Takes to long time to do full
        # service.write_to_db_baseschema(sample=True)

    def test_upwrite_to_db(self):
        from MetaDataApi.metadata.services import (
            JsonSchemaService)

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/" +\
            "master/schemas/json/omh/schemas/acceleration-1.0.json"

        service = JsonSchemaService()

        objects = service.write_to_db(url, "open_m_health")

        labels = list(map(lambda x: x.label, objects))

        labels_compare = [
            "open_m_health", "acceleration", "acceleration_x",
            "acceleration_x", "acceleration_x", "acceleration_y",
            "acceleration_y", "acceleration_y", "acceleration_z",
            "acceleration_z", "acceleration_z", "effective_time_frame",
            "effective_time_frame", "date_time", "time_interval",
            "time_interval", "start_date_time", "duration", "duration",
            "duration", "end_date_time", "duration", "duration",
            "start_date_time", "end_date_time", "part_of_day",
            "sensor_body_location", "descriptive_statistic"]

        labels = list(set(labels))
        labels_compare = list(set(labels_compare))

        labels.sort()
        labels_compare.sort()

        self.assertListEqual(labels, labels_compare)

    def test_json_write_to_db_body_temp(self):
        from MetaDataApi.metadata.services import (
            JsonSchemaService)
        from MetaDataApi.metadata.models import (
            Schema, Object, Attribute, ObjectRelation)

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/" +\
            "master/schemas/json/omh/schemas/body-temperature-2.0.json"

        service = JsonSchemaService()

        res = service.write_to_db(url, "open_m_health")

        atts = filter(lambda x: isinstance(x, Attribute), res)

    def test_default_schemas(self):
        from MetaDataApi.metadata.services import (
            JsonSchemaService)

        service = JsonSchemaService()
        # Takes to long time to do full
        service.write_to_db_baseschema(sample=True)

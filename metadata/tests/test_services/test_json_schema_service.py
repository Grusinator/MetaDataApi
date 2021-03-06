import unittest

import django
from django.conf import settings
from django.test import TransactionTestCase

from metadata.tests.data import LoadTestData

TAGS = set("rdf")


class TestJsonService(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestJsonService, cls).setUpClass()
        django.setup()

        LoadTestData.init_foaf()

        LoadTestData.init_open_m_health_sample()

    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    def test_upwrite_to_db(self):
        from metadata.services import (
            JsonSchemaService)

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/" + \
              "master/schemas/json/omh/schemas/acceleration-1.0.json"

        service = JsonSchemaService()

        objects = service.write_to_db(url, "open_m_health")

        labels = list(map(lambda x: x.label, objects))

        labels_compare = [
            "acceleration", "acceleration_x",
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
        from metadata.services import (
            JsonSchemaService)
        from metadata.models import (
            SchemaAttribute)

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/" + \
              "master/schemas/json/omh/schemas/body-temperature-2.0.json"

        service = JsonSchemaService()

        res = service.write_to_db(url, "open_m_health")

        atts = filter(lambda x: isinstance(x, SchemaAttribute), res)

    @unittest.skip
    def test_default_schemas(self):
        from metadata.services import (
            JsonSchemaService)

        service = JsonSchemaService()
        # Takes to long time to do full
        service.write_to_db_baseschema(sample=True)

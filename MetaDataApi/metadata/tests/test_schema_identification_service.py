import json
from urllib import request

import django
from django.test import TransactionTestCase

from metadata.tests.data import LoadTestData
from metadata.tests.utils_for_testing.common_utils_for_testing import UtilsForTesting


class TestSchemaIdentificationService(TransactionTestCase):
    """Tests for the application views."""
    # fixtures = [
    #     'metadata/fixtures/new_load.json',
    # ]

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestSchemaIdentificationService, cls).setUpClass()
        django.setup()

    def test_identify_json_data_sample(self):
        from metadata.services import (
            JsonAnalyser)

        from metadata.models import Schema, Object

        user = LoadTestData.init_user()
        LoadTestData.init_foaf()


        LoadTestData.init_open_m_health_sample(extras=[
            "body-temperature-2.0.json",
            "body-temperature-2.x.json",
        ])

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi" + \
            "/master/schemas/json/omh/test_data/body-temperature/2.0/" + \
            "shouldPass/valid-temperature.json"

        obj_count = Object.objects.all().count()
        # make sure that the number of objects is larger than
        if obj_count < 10:
            raise AssertionError("database not populated")

        with request.urlopen(url) as resp:
            text = resp.read().decode()

        service = JsonAnalyser()
        schema = service.do_meta_item_exists(Schema(label="open_m_health"))

        input_data = {
            "body-temperature": json.loads(text)
        }

        objs = service.identify_from_json_data(input_data, schema, user, "body-temperature")

        compare_instances = ['Oi:open_m_health.body-temperature',
                             'Ri:person - person__to__body-temperature - body-temperature',
                             'Oi:open_m_health.body-temperature',
                             'Ri:body-temperature - body-temperature__to__body-temperature - body-temperature',
                             'Ai:body-temperature.body_temperature:97', 'Oi:open_m_health.effective_time_frame',
                             'Ri:body-temperature - body-temperature__to__effective_time_frame - effective_time_frame',
                             'Ai:effective_time_frame.date_time:2013-02-05T07:25:00Z',
                             'Ai:body-temperature.measurement_location:forehead']

        instance_str = [str(obj) for obj in objs]

        self.assertListEqual(compare_instances, instance_str)

    def test_identify_data_type(self):
        from metadata.services import (
            JsonAnalyser)
        from datetime import datetime

        input_vs_expected = [
            ("20.40", float),
            (2.4, float),
            ("2012-01-19 17:21:00", datetime),
            ('2018-10-02T16: 16: 49Z', datetime),
            # ("2019-20-04:20:30:59", datetime),
            (2, int),
            ("1", int),
            ("test", str),
            ("False", bool),
            (True, bool),
            (None, type(None))
        ]

        inputd, expected = zip(*input_vs_expected)

        service = JsonAnalyser()

        resp = [type(service.identify_data_type(elm)) for elm in inputd]

        self.assertListEqual(list(resp), list(expected))

    def test_identify_from_json_data_strava_test(self):
        from metadata.services import (
            RdfSchemaService, JsonAnalyser, RdfInstanceService)

        from metadata.models import Schema, Object, Attribute, ObjectRelation

        rdf_inst = RdfInstanceService()

        # data_cleaning = DataCleaningService()

        LoadTestData.init_foaf()

        user = LoadTestData.init_user()

        # schema = LoadTestData.init_strava_schema_from_file()

        schema = Schema(label="strava")
        schema.save()

        # objects = LoadTestData.init_strava_data_from_file()

        service = JsonAnalyser()

        data = UtilsForTesting.loadStravaActivities()

        objects = service.identify_from_json_data(
            data, schema, user, parrent_label="activities")

        metaobj = list(Object.objects.all())
        metaobj = list(ObjectRelation.objects.all())
        metaobj = list(Attribute.objects.all())

        labels = list(map(lambda x: "%s - %s" %
                          (x.base.label, str(type(x).__name__)), objects))

        RdfSchemaService().export_schema_from_db(schema)

        file = RdfInstanceService().export_instances_to_rdf_file(schema, objects)

        print(schema.url)

        expected = ['activities - ObjectInstance', 'person__to__activities - ObjectRelationInstance', 'athlete - ObjectInstance', 'activities__to__athlete - ObjectRelationInstance', 'start_latlng - ObjectInstance', 'activities__to__start_latlng - ObjectRelationInstance', 'start_latlng - FloatAttributeInstance', 'end_latlng - ObjectInstance', 'activities__to__end_latlng - ObjectRelationInstance', 'end_latlng - FloatAttributeInstance', 'location_city - ObjectInstance', 'activities__to__location_city - ObjectRelationInstance', 'location_state - ObjectInstance', 'activities__to__location_state - ObjectRelationInstance', 'map - ObjectInstance', 'activities__to__map - ObjectRelationInstance', 'gear_id - ObjectInstance', 'activities__to__gear_id - ObjectRelationInstance', 'activities - ObjectInstance', 'resource_state - IntAttributeInstance', 'athlete - ObjectInstance', 'id - IntAttributeInstance', 'resource_state - IntAttributeInstance', 'name - StringAttributeInstance', 'distance - FloatAttributeInstance', 'moving_time - IntAttributeInstance', 'elapsed_time - IntAttributeInstance', 'total_elevation_gain - FloatAttributeInstance', 'type - StringAttributeInstance', 'workout_type - IntAttributeInstance', 'id - IntAttributeInstance', 'external_id - StringAttributeInstance', 'upload_id - IntAttributeInstance', 'start_date - DateTimeAttributeInstance', 'start_date_local - DateTimeAttributeInstance', 'timezone - StringAttributeInstance', 'utc_offset - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'location_country - StringAttributeInstance', 'start_latitude - FloatAttributeInstance', 'start_longitude - FloatAttributeInstance', 'achievement_count - IntAttributeInstance', 'kudos_count - IntAttributeInstance', 'comment_count - IntAttributeInstance', 'athlete_count - IntAttributeInstance', 'photo_count - IntAttributeInstance', 'map - ObjectInstance', 'id - StringAttributeInstance', 'summary_polyline - StringAttributeInstance', 'resource_state - IntAttributeInstance', 'trainer - BoolAttributeInstance', 'commute - BoolAttributeInstance', 'manual - BoolAttributeInstance', 'private - BoolAttributeInstance', 'visibility - StringAttributeInstance', 'flagged - BoolAttributeInstance', 'from_accepted_tag - BoolAttributeInstance', 'average_speed - FloatAttributeInstance', 'max_speed - FloatAttributeInstance', 'has_heartrate - BoolAttributeInstance', 'heartrate_opt_out - BoolAttributeInstance', 'display_hide_heartrate_option - BoolAttributeInstance', 'elev_high - FloatAttributeInstance', 'elev_low - FloatAttributeInstance', 'pr_count - IntAttributeInstance', 'total_photo_count - IntAttributeInstance', 'has_kudoed - BoolAttributeInstance', 'activities - ObjectInstance', 'resource_state - IntAttributeInstance', 'athlete - ObjectInstance', 'id - IntAttributeInstance', 'resource_state - IntAttributeInstance', 'name - StringAttributeInstance', 'distance - FloatAttributeInstance', 'moving_time - IntAttributeInstance', 'elapsed_time - IntAttributeInstance', 'total_elevation_gain - FloatAttributeInstance', 'type - StringAttributeInstance', 'workout_type - IntAttributeInstance', 'id - IntAttributeInstance', 'external_id - StringAttributeInstance', 'upload_id - IntAttributeInstance', 'start_date - DateTimeAttributeInstance', 'start_date_local - DateTimeAttributeInstance', 'timezone - StringAttributeInstance', 'utc_offset - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'location_country - StringAttributeInstance', 'start_latitude - FloatAttributeInstance', 'start_longitude - FloatAttributeInstance', 'achievement_count - IntAttributeInstance', 'kudos_count - IntAttributeInstance', 'comment_count - IntAttributeInstance', 'athlete_count - IntAttributeInstance', 'photo_count - IntAttributeInstance', 'map - ObjectInstance', 'id - StringAttributeInstance', 'summary_polyline - StringAttributeInstance', 'resource_state - IntAttributeInstance', 'trainer - BoolAttributeInstance', 'commute - BoolAttributeInstance', 'manual - BoolAttributeInstance', 'private - BoolAttributeInstance', 'visibility - StringAttributeInstance', 'flagged - BoolAttributeInstance', 'from_accepted_tag - BoolAttributeInstance', 'average_speed - FloatAttributeInstance', 'max_speed - FloatAttributeInstance', 'has_heartrate - BoolAttributeInstance', 'heartrate_opt_out - BoolAttributeInstance', 'display_hide_heartrate_option - BoolAttributeInstance', 'elev_high - FloatAttributeInstance', 'elev_low - FloatAttributeInstance', 'pr_count - IntAttributeInstance', 'total_photo_count - IntAttributeInstance', 'has_kudoed - BoolAttributeInstance', 'activities - ObjectInstance', 'resource_state - IntAttributeInstance', 'athlete - ObjectInstance', 'id - IntAttributeInstance', 'resource_state - IntAttributeInstance', 'name - StringAttributeInstance', 'distance - FloatAttributeInstance', 'moving_time - IntAttributeInstance', 'elapsed_time - IntAttributeInstance', 'total_elevation_gain - FloatAttributeInstance', 'type - StringAttributeInstance', 'workout_type - IntAttributeInstance', 'id - IntAttributeInstance', 'external_id - StringAttributeInstance', 'upload_id - IntAttributeInstance', 'start_date - DateTimeAttributeInstance', 'start_date_local - DateTimeAttributeInstance', 'timezone - StringAttributeInstance', 'utc_offset - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'location_country - StringAttributeInstance', 'start_latitude - FloatAttributeInstance', 'start_longitude - FloatAttributeInstance', 'achievement_count - IntAttributeInstance', 'kudos_count - IntAttributeInstance', 'comment_count - IntAttributeInstance', 'athlete_count - IntAttributeInstance', 'photo_count - IntAttributeInstance', 'map - ObjectInstance', 'id - StringAttributeInstance', 'summary_polyline - StringAttributeInstance', 'resource_state - IntAttributeInstance', 'trainer - BoolAttributeInstance', 'commute - BoolAttributeInstance', 'manual - BoolAttributeInstance', 'private - BoolAttributeInstance', 'visibility - StringAttributeInstance', 'flagged - BoolAttributeInstance', 'from_accepted_tag - BoolAttributeInstance',
                    'average_speed - FloatAttributeInstance', 'max_speed - FloatAttributeInstance', 'has_heartrate - BoolAttributeInstance', 'heartrate_opt_out - BoolAttributeInstance', 'display_hide_heartrate_option - BoolAttributeInstance', 'elev_high - FloatAttributeInstance', 'elev_low - FloatAttributeInstance', 'pr_count - IntAttributeInstance', 'total_photo_count - IntAttributeInstance', 'has_kudoed - BoolAttributeInstance', 'activities - ObjectInstance', 'resource_state - IntAttributeInstance', 'athlete - ObjectInstance', 'id - IntAttributeInstance', 'resource_state - IntAttributeInstance', 'name - StringAttributeInstance', 'distance - FloatAttributeInstance', 'moving_time - IntAttributeInstance', 'elapsed_time - IntAttributeInstance', 'total_elevation_gain - FloatAttributeInstance', 'type - StringAttributeInstance', 'workout_type - IntAttributeInstance', 'id - IntAttributeInstance', 'external_id - StringAttributeInstance', 'upload_id - IntAttributeInstance', 'start_date - DateTimeAttributeInstance', 'start_date_local - DateTimeAttributeInstance', 'timezone - StringAttributeInstance', 'utc_offset - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'location_country - StringAttributeInstance', 'start_latitude - FloatAttributeInstance', 'start_longitude - FloatAttributeInstance', 'achievement_count - IntAttributeInstance', 'kudos_count - IntAttributeInstance', 'comment_count - IntAttributeInstance', 'athlete_count - IntAttributeInstance', 'photo_count - IntAttributeInstance', 'map - ObjectInstance', 'id - StringAttributeInstance', 'resource_state - IntAttributeInstance', 'trainer - BoolAttributeInstance', 'commute - BoolAttributeInstance', 'manual - BoolAttributeInstance', 'private - BoolAttributeInstance', 'visibility - StringAttributeInstance', 'flagged - BoolAttributeInstance', 'from_accepted_tag - BoolAttributeInstance', 'average_speed - FloatAttributeInstance', 'max_speed - FloatAttributeInstance', 'has_heartrate - BoolAttributeInstance', 'heartrate_opt_out - BoolAttributeInstance', 'display_hide_heartrate_option - BoolAttributeInstance', 'elev_high - FloatAttributeInstance', 'elev_low - FloatAttributeInstance', 'pr_count - IntAttributeInstance', 'total_photo_count - IntAttributeInstance', 'has_kudoed - BoolAttributeInstance', 'activities - ObjectInstance', 'resource_state - IntAttributeInstance', 'athlete - ObjectInstance', 'id - IntAttributeInstance', 'resource_state - IntAttributeInstance', 'name - StringAttributeInstance', 'distance - FloatAttributeInstance', 'moving_time - IntAttributeInstance', 'elapsed_time - IntAttributeInstance', 'total_elevation_gain - FloatAttributeInstance', 'type - StringAttributeInstance', 'workout_type - IntAttributeInstance', 'id - IntAttributeInstance', 'external_id - StringAttributeInstance', 'upload_id - IntAttributeInstance', 'start_date - DateTimeAttributeInstance', 'start_date_local - DateTimeAttributeInstance', 'timezone - StringAttributeInstance', 'utc_offset - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'location_country - StringAttributeInstance', 'start_latitude - FloatAttributeInstance', 'start_longitude - FloatAttributeInstance', 'achievement_count - IntAttributeInstance', 'kudos_count - IntAttributeInstance', 'comment_count - IntAttributeInstance', 'athlete_count - IntAttributeInstance', 'photo_count - IntAttributeInstance', 'map - ObjectInstance', 'id - StringAttributeInstance', 'summary_polyline - StringAttributeInstance', 'resource_state - IntAttributeInstance', 'trainer - BoolAttributeInstance', 'commute - BoolAttributeInstance', 'manual - BoolAttributeInstance', 'private - BoolAttributeInstance', 'visibility - StringAttributeInstance', 'flagged - BoolAttributeInstance', 'from_accepted_tag - BoolAttributeInstance', 'average_speed - FloatAttributeInstance', 'max_speed - FloatAttributeInstance', 'has_heartrate - BoolAttributeInstance', 'heartrate_opt_out - BoolAttributeInstance', 'display_hide_heartrate_option - BoolAttributeInstance', 'elev_high - FloatAttributeInstance', 'elev_low - FloatAttributeInstance', 'pr_count - IntAttributeInstance', 'total_photo_count - IntAttributeInstance', 'has_kudoed - BoolAttributeInstance', 'activities - ObjectInstance', 'resource_state - IntAttributeInstance', 'athlete - ObjectInstance', 'id - IntAttributeInstance', 'resource_state - IntAttributeInstance', 'name - StringAttributeInstance', 'distance - FloatAttributeInstance', 'moving_time - IntAttributeInstance', 'elapsed_time - IntAttributeInstance', 'total_elevation_gain - FloatAttributeInstance', 'type - StringAttributeInstance', 'workout_type - IntAttributeInstance', 'id - IntAttributeInstance', 'external_id - StringAttributeInstance', 'upload_id - IntAttributeInstance', 'start_date - DateTimeAttributeInstance', 'start_date_local - DateTimeAttributeInstance', 'timezone - StringAttributeInstance', 'utc_offset - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'start_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'end_latlng - FloatAttributeInstance', 'location_country - StringAttributeInstance', 'start_latitude - FloatAttributeInstance', 'start_longitude - FloatAttributeInstance', 'achievement_count - IntAttributeInstance', 'kudos_count - IntAttributeInstance', 'comment_count - IntAttributeInstance', 'athlete_count - IntAttributeInstance', 'photo_count - IntAttributeInstance', 'map - ObjectInstance', 'id - StringAttributeInstance', 'summary_polyline - StringAttributeInstance', 'resource_state - IntAttributeInstance', 'trainer - BoolAttributeInstance', 'commute - BoolAttributeInstance', 'manual - BoolAttributeInstance', 'private - BoolAttributeInstance', 'visibility - StringAttributeInstance', 'flagged - BoolAttributeInstance', 'from_accepted_tag - BoolAttributeInstance', 'average_speed - FloatAttributeInstance', 'max_speed - FloatAttributeInstance', 'has_heartrate - BoolAttributeInstance', 'heartrate_opt_out - BoolAttributeInstance', 'display_hide_heartrate_option - BoolAttributeInstance', 'elev_high - FloatAttributeInstance', 'elev_low - FloatAttributeInstance', 'pr_count - IntAttributeInstance', 'total_photo_count - IntAttributeInstance', 'has_kudoed - BoolAttributeInstance']

        labels.sort()
        expected.sort()

        self.assertEqual(labels, expected)

    def test_identify_from_json_data(self):
        from metadata.services import (
            RdfSchemaService, DataCleaningService,
            RdfInstanceService)

        rdf_inst = RdfInstanceService()

        data_cleaning = DataCleaningService()

        LoadTestData.init_foaf()

        schema = LoadTestData.init_strava_schema_from_file()

        objects = LoadTestData.init_strava_data_from_file()

        RdfSchemaService().export_schema_from_db(schema)

        file = RdfInstanceService().export_instances_to_rdf_file(schema, objects)

        print(schema.url)

        self.assertGreater(len(objects), 10)

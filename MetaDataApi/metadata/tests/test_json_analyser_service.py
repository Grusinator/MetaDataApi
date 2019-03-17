import json
from urllib import request

import django
from django.test import TransactionTestCase

from metadata.tests.data import LoadTestData
from metadata.tests.utils_for_testing.common_utils_for_testing import UtilsForTesting


class TestSchemaIdentificationService(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSchemaIdentificationService, cls).setUpClass()
        django.setup()

    def test_identify_json_data_sample(self):
        from metadata.services import (
            JsonAnalyser)

        from metadata.models import Schema

        user = LoadTestData.init_user()
        LoadTestData.init_foaf()

        LoadTestData.init_open_m_health_sample(extras=[
            "body-temperature-2.0.json",
            "body-temperature-2.x.json",
        ])

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi" + \
              "/master/schemas/json/omh/test_data/body-temperature/2.0/" + \
              "shouldPass/valid-temperature.json"

        with request.urlopen(url) as resp:
            text = resp.read().decode()

        service = JsonAnalyser()
        schema = Schema.objects.get(label="open_m_health")

        input_data = {
            "body-temperature": json.loads(text)
        }

        instances = service.identify_from_json_data(input_data, schema, user, "body-temperature")

        labels = UtilsForTesting.build_meta_instance_strings_for_comparison(instances)

        expected = self.open_m_health()

        self.assertEqual(labels, expected)

    def test_identify_from_json_data_strava_test(self):
        from metadata.services import (
            JsonAnalyser)
        from metadata.models import Schema

        LoadTestData.init_foaf()
        user = LoadTestData.init_user()
        schema = Schema(label="strava")
        schema.save()

        data = LoadTestData.loadStravaActivities()

        service = JsonAnalyser()
        instances = service.identify_from_json_data(
            data, schema, user, parrent_label="activities")

        labels = UtilsForTesting.build_meta_instance_strings_for_comparison(instances)

        expected = self.expected_strava_instances()

        self.assertEqual(labels, expected)

    @staticmethod
    def expected_strava_instances():
        return ['achievement_count - IntAttributeInstance : 0', 'achievement_count - IntAttributeInstance : 11',
                'activities - ObjectInstance', 'activities__to__athlete - ObjectRelationInstance',
                'activities__to__end_latlng - ObjectRelationInstance',
                'activities__to__gear_id - ObjectRelationInstance',
                'activities__to__location_city - ObjectRelationInstance',
                'activities__to__location_state - ObjectRelationInstance',
                'activities__to__map - ObjectRelationInstance', 'activities__to__start_latlng - ObjectRelationInstance',
                'athlete - ObjectInstance', 'athlete_count - IntAttributeInstance : 1',
                'athlete_count - IntAttributeInstance : 2', 'average_speed - FloatAttributeInstance : 3.065',
                'average_speed - FloatAttributeInstance : 3.081', 'average_speed - FloatAttributeInstance : 3.126',
                'average_speed - FloatAttributeInstance : 3.154', 'average_speed - FloatAttributeInstance : 3.286',
                'average_speed - FloatAttributeInstance : 4.033', 'average_speed - FloatAttributeInstance : 5.198',
                'comment_count - IntAttributeInstance : 0', 'comment_count - IntAttributeInstance : 1',
                'commute - BoolAttributeInstance : False',
                'display_hide_heartrate_option - BoolAttributeInstance : False',
                'distance - FloatAttributeInstance : 11867.8', 'distance - FloatAttributeInstance : 3133.3',
                'distance - FloatAttributeInstance : 3503.7', 'distance - FloatAttributeInstance : 3555.6',
                'distance - FloatAttributeInstance : 3926.8', 'distance - FloatAttributeInstance : 4395.6',
                'distance - FloatAttributeInstance : 4774.5', 'elapsed_time - IntAttributeInstance : 1257',
                'elapsed_time - IntAttributeInstance : 1695', 'elapsed_time - IntAttributeInstance : 1765',
                'elapsed_time - IntAttributeInstance : 1821', 'elapsed_time - IntAttributeInstance : 1848',
                'elapsed_time - IntAttributeInstance : 2149', 'elapsed_time - IntAttributeInstance : 660103',
                'elev_high - FloatAttributeInstance : 12.4', 'elev_high - FloatAttributeInstance : 13.0',
                'elev_high - FloatAttributeInstance : 18.0', 'elev_high - FloatAttributeInstance : 66.0',
                'elev_low - FloatAttributeInstance : 4.5', 'elev_low - FloatAttributeInstance : 5.0',
                'elev_low - FloatAttributeInstance : 5.3', 'elev_low - FloatAttributeInstance : 52.6',
                'elev_low - FloatAttributeInstance : 6.0', 'end_latlng - FloatAttributeInstance : 12.567028',
                'end_latlng - FloatAttributeInstance : 12.567233', 'end_latlng - FloatAttributeInstance : 12.574356',
                'end_latlng - FloatAttributeInstance : 12.574467', 'end_latlng - FloatAttributeInstance : 12.574542',
                'end_latlng - FloatAttributeInstance : 12.574554', 'end_latlng - FloatAttributeInstance : 55.721795',
                'end_latlng - FloatAttributeInstance : 55.726303', 'end_latlng - FloatAttributeInstance : 55.7277',
                'end_latlng - FloatAttributeInstance : 55.72773', 'end_latlng - FloatAttributeInstance : 55.7278',
                'end_latlng - FloatAttributeInstance : 55.727854', 'end_latlng - FloatAttributeInstance : 55.82314',
                'end_latlng - FloatAttributeInstance : 9.105082', 'end_latlng - ObjectInstance',
                'external_id - StringAttributeInstance : 0446b183956a4246b509e8178d962a73',
                'external_id - StringAttributeInstance : 05a1170cb9421acf012cb660809f8707',
                'external_id - StringAttributeInstance : 05c7eb647109b6c780272927a052d65d',
                'external_id - StringAttributeInstance : 1a9455a9ebbc7a2c0bf0beea64daaa30',
                'external_id - StringAttributeInstance : c28d5d8cb5f87f647b2c1fa8d3ffcd15',
                'external_id - StringAttributeInstance : d991414cf07af9be57fbd0e74a89d8a4',
                'external_id - StringAttributeInstance : dffe18b96bfe979f96633d7a21930813',
                'flagged - BoolAttributeInstance : False', 'from_accepted_tag - BoolAttributeInstance : False',
                'gear_id - ObjectInstance', 'has_heartrate - BoolAttributeInstance : False',
                'has_kudoed - BoolAttributeInstance : False', 'heartrate_opt_out - BoolAttributeInstance : False',
                'id - IntAttributeInstance : 1853632245', 'id - IntAttributeInstance : 1853676308',
                'id - IntAttributeInstance : 1862269980', 'id - IntAttributeInstance : 1866238587',
                'id - IntAttributeInstance : 1870572749', 'id - IntAttributeInstance : 1874410370',
                'id - IntAttributeInstance : 1879752969', 'id - IntAttributeInstance : 465645',
                'id - StringAttributeInstance : a1853632245', 'id - StringAttributeInstance : a1853676308',
                'id - StringAttributeInstance : a1862269980', 'id - StringAttributeInstance : a1866238587',
                'id - StringAttributeInstance : a1870572749', 'id - StringAttributeInstance : a1874410370',
                'id - StringAttributeInstance : a1879752969', 'kudos_count - IntAttributeInstance : 0',
                'kudos_count - IntAttributeInstance : 1', 'kudos_count - IntAttributeInstance : 2',
                'location_city - ObjectInstance', 'location_country - StringAttributeInstance : Denmark',
                'location_state - ObjectInstance', 'manual - BoolAttributeInstance : False', 'map - ObjectInstance',
                'max_speed - FloatAttributeInstance : 10.7', 'max_speed - FloatAttributeInstance : 11.3',
                'max_speed - FloatAttributeInstance : 14.0', 'max_speed - FloatAttributeInstance : 4.0',
                'max_speed - FloatAttributeInstance : 5.6', 'max_speed - FloatAttributeInstance : 9.0',
                'max_speed - FloatAttributeInstance : 9.4', 'moving_time - IntAttributeInstance : 1143',
                'moving_time - IntAttributeInstance : 1154', 'moving_time - IntAttributeInstance : 1195',
                'moving_time - IntAttributeInstance : 1406', 'moving_time - IntAttributeInstance : 1514',
                'moving_time - IntAttributeInstance : 2283', 'moving_time - IntAttributeInstance : 777',
                'name - StringAttributeInstance : 8 x ~30 sek interval med bakke',
                'name - StringAttributeInstance : 8x30 sek interval',
                'name - StringAttributeInstance : 9 x ~30 sek interval', 'name - StringAttributeInstance : Evening Run',
                'name - StringAttributeInstance : LÃ¸b med phillip', 'name - StringAttributeInstance : Morgen',
                'name - StringAttributeInstance : Morning Run', 'person__to__activities - ObjectRelationInstance',
                'photo_count - IntAttributeInstance : 0', 'pr_count - IntAttributeInstance : 0',
                'pr_count - IntAttributeInstance : 5', 'private - BoolAttributeInstance : False',
                'private - BoolAttributeInstance : True', 'resource_state - IntAttributeInstance : 1',
                'resource_state - IntAttributeInstance : 2',
                'start_date - DateTimeAttributeInstance : 2018-09-12 15:09:44',
                'start_date - DateTimeAttributeInstance : 2018-09-20 06:30:42',
                'start_date - DateTimeAttributeInstance : 2018-09-24 07:45:02',
                'start_date - DateTimeAttributeInstance : 2018-09-26 05:45:27',
                'start_date - DateTimeAttributeInstance : 2018-09-28 08:59:08',
                'start_date - DateTimeAttributeInstance : 2018-09-30 06:29:17',
                'start_date - DateTimeAttributeInstance : 2018-10-02 16:16:49',
                'start_date_local - DateTimeAttributeInstance : 2018-09-12 17:09:44',
                'start_date_local - DateTimeAttributeInstance : 2018-09-20 08:30:42',
                'start_date_local - DateTimeAttributeInstance : 2018-09-24 09:45:02',
                'start_date_local - DateTimeAttributeInstance : 2018-09-26 07:45:27',
                'start_date_local - DateTimeAttributeInstance : 2018-09-28 10:59:08',
                'start_date_local - DateTimeAttributeInstance : 2018-09-30 08:29:17',
                'start_date_local - DateTimeAttributeInstance : 2018-10-02 18:16:49',
                'start_latitude - FloatAttributeInstance : 55.694375',
                'start_latitude - FloatAttributeInstance : 55.727547',
                'start_latitude - FloatAttributeInstance : 55.727747',
                'start_latitude - FloatAttributeInstance : 55.727841',
                'start_latitude - FloatAttributeInstance : 55.72792',
                'start_latitude - FloatAttributeInstance : 55.727978',
                'start_latitude - FloatAttributeInstance : 55.823333',
                'start_latlng - FloatAttributeInstance : 12.57413', 'start_latlng - FloatAttributeInstance : 12.574154',
                'start_latlng - FloatAttributeInstance : 12.574233',
                'start_latlng - FloatAttributeInstance : 12.574337',
                'start_latlng - FloatAttributeInstance : 12.574341',
                'start_latlng - FloatAttributeInstance : 12.586909',
                'start_latlng - FloatAttributeInstance : 55.694375',
                'start_latlng - FloatAttributeInstance : 55.727547',
                'start_latlng - FloatAttributeInstance : 55.727747',
                'start_latlng - FloatAttributeInstance : 55.727841', 'start_latlng - FloatAttributeInstance : 55.72792',
                'start_latlng - FloatAttributeInstance : 55.727978',
                'start_latlng - FloatAttributeInstance : 55.823333', 'start_latlng - FloatAttributeInstance : 9.105255',
                'start_latlng - ObjectInstance', 'start_longitude - FloatAttributeInstance : 12.57413',
                'start_longitude - FloatAttributeInstance : 12.574154',
                'start_longitude - FloatAttributeInstance : 12.574233',
                'start_longitude - FloatAttributeInstance : 12.574337',
                'start_longitude - FloatAttributeInstance : 12.574341',
                'start_longitude - FloatAttributeInstance : 12.586909',
                'start_longitude - FloatAttributeInstance : 9.105255',
                'summary_polyline - StringAttributeInstance : _jcsIs|vkAy@jA~GEaC`b@d@dFjHJzD_DzHlAj@xIxCjHvCoA|AsF|Aj@qHqGfH`IcGmH',
                'summary_polyline - StringAttributeInstance : chcsIi{vkApCh@gBl^T`B~@VCaBD|E~UbI`CfGnG|DfBYvAgGgKqL{OwAl@dFhHrA`@aG|@c@~I`Hq@`GeFzCwDwKeGs@{AkD}FZ',
                'summary_polyline - StringAttributeInstance : kicsI}{vkAbD~@kBz[l@nCoAxFlFEvA`CbUuDvLjKnTd\\\\gFqG_EpH{KbDgG}HqNy@{Q_Hd@_[{E_D`FoAjAmHr@mSiD}@P}A',
                'summary_polyline - StringAttributeInstance : ojcsIm{vkAvFKaChi@fYbH|EtIdCoBpD|BtAkEeKtEeBaAoBqHFqHxAOzDnEdAfHxAcDaJkIk\\\\TYcHfCg^sEiB',
                'summary_polyline - StringAttributeInstance : yjcsIq|vkAjF`AsCdd@fG~CnKCe@fAlCaC{D~@lAIi@rAfAaB{BVxBc@aCXbCUuBZx@OQ|ApAgBsBXpBc@iI`AcJ}Ca@qB|@cBjBq]mDaB',
                'summary_polyline - StringAttributeInstance : yx|rIckykAtE~GyA~GmK~U}WxObAbGkSje@nAnC{CvHTfChFxEdKhBxCcDpHwXqBmJyJWcRv[ZdCfFvE`LtAhCuD~GgX}CgKiIZwN|TvNbUmNiU{BzEdFrIrGxBfGsCbEqLz@uKsY|EI{EnR{d@EcGlPkI_dEj^',
                'timezone - StringAttributeInstance : (GMT+01: 00) Europe/Copenhagen',
                'total_elevation_gain - FloatAttributeInstance : 11.1',
                'total_elevation_gain - FloatAttributeInstance : 13.2',
                'total_elevation_gain - FloatAttributeInstance : 14.0',
                'total_elevation_gain - FloatAttributeInstance : 22.0',
                'total_elevation_gain - FloatAttributeInstance : 27.3',
                'total_elevation_gain - FloatAttributeInstance : 27.7',
                'total_elevation_gain - FloatAttributeInstance : 51.9', 'total_photo_count - IntAttributeInstance : 0',
                'trainer - BoolAttributeInstance : False', 'type - StringAttributeInstance : Run',
                'upload_id - IntAttributeInstance : 1986336755', 'upload_id - IntAttributeInstance : 1986381489',
                'upload_id - IntAttributeInstance : 1995341066', 'upload_id - IntAttributeInstance : 1999406897',
                'upload_id - IntAttributeInstance : 2003860523', 'upload_id - IntAttributeInstance : 2007831642',
                'upload_id - IntAttributeInstance : 2013405598', 'utc_offset - FloatAttributeInstance : 7200.0',
                'visibility - StringAttributeInstance : everyone', 'visibility - StringAttributeInstance : only_me',
                'workout_type - IntAttributeInstance : 0', 'workout_type - IntAttributeInstance : 3']

    @staticmethod
    def open_m_health():
        return ['body-temperature - ObjectInstance', 'body-temperature__to__body-temperature - ObjectRelationInstance',
                'body-temperature__to__effective_time_frame - ObjectRelationInstance',
                'body_temperature - IntAttributeInstance : 97',
                'date_time - DateTimeAttributeInstance : 2013-02-05 07:25:00+00:00',
                'effective_time_frame - ObjectInstance', 'measurement_location - StringAttributeInstance : forehead',
                'person__to__body-temperature - ObjectRelationInstance']

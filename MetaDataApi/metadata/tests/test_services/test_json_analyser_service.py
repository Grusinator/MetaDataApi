import json
from urllib import request

import django
from django.test import TransactionTestCase

from MetaDataApi.metadata.tests.data import LoadTestData
from MetaDataApi.metadata.tests.utils_for_testing.common_utils_for_testing import UtilsForTesting


class TestSchemaIdentificationService(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSchemaIdentificationService, cls).setUpClass()
        django.setup()

    def test_identify_json_data_sample(self):
        from MetaDataApi.metadata.services import (
            JsonAnalyser)

        from MetaDataApi.metadata.models import Schema

        user = LoadTestData.init_user()
        LoadTestData.init_profile(user)
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
        from MetaDataApi.metadata.services import (
            JsonAnalyser)
        from MetaDataApi.metadata.models import Schema

        LoadTestData.init_foaf()
        user = LoadTestData.init_user()
        LoadTestData.init_profile(user)
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
        return ['achievement_count - IntAttribute : 0', 'achievement_count - IntAttribute : 11',
                'activities - Node', 'activities__to__athlete - Edge',
                'activities__to__end_latlng - Edge',
                'activities__to__gear_id - Edge',
                'activities__to__location_city - Edge',
                'activities__to__location_state - Edge',
                'activities__to__map - Edge', 'activities__to__start_latlng - Edge',
                'athlete - Node', 'athlete_count - IntAttribute : 1',
                'athlete_count - IntAttribute : 2', 'average_speed - FloatAttribute : 3.065',
                'average_speed - FloatAttribute : 3.081', 'average_speed - FloatAttribute : 3.126',
                'average_speed - FloatAttribute : 3.154', 'average_speed - FloatAttribute : 3.286',
                'average_speed - FloatAttribute : 4.033', 'average_speed - FloatAttribute : 5.198',
                'comment_count - IntAttribute : 0', 'comment_count - IntAttribute : 1',
                'commute - BoolAttribute : False',
                'display_hide_heartrate_option - BoolAttribute : False',
                'distance - FloatAttribute : 11867.8', 'distance - FloatAttribute : 3133.3',
                'distance - FloatAttribute : 3503.7', 'distance - FloatAttribute : 3555.6',
                'distance - FloatAttribute : 3926.8', 'distance - FloatAttribute : 4395.6',
                'distance - FloatAttribute : 4774.5', 'elapsed_time - IntAttribute : 1257',
                'elapsed_time - IntAttribute : 1695', 'elapsed_time - IntAttribute : 1765',
                'elapsed_time - IntAttribute : 1821', 'elapsed_time - IntAttribute : 1848',
                'elapsed_time - IntAttribute : 2149', 'elapsed_time - IntAttribute : 660103',
                'elev_high - FloatAttribute : 12.4', 'elev_high - FloatAttribute : 13.0',
                'elev_high - FloatAttribute : 18.0', 'elev_high - FloatAttribute : 66.0',
                'elev_low - FloatAttribute : 4.5', 'elev_low - FloatAttribute : 5.0',
                'elev_low - FloatAttribute : 5.3', 'elev_low - FloatAttribute : 52.6',
                'elev_low - FloatAttribute : 6.0', 'end_latlng - FloatAttribute : 12.567028',
                'end_latlng - FloatAttribute : 12.567233', 'end_latlng - FloatAttribute : 12.574356',
                'end_latlng - FloatAttribute : 12.574467', 'end_latlng - FloatAttribute : 12.574542',
                'end_latlng - FloatAttribute : 12.574554', 'end_latlng - FloatAttribute : 55.721795',
                'end_latlng - FloatAttribute : 55.726303', 'end_latlng - FloatAttribute : 55.7277',
                'end_latlng - FloatAttribute : 55.72773', 'end_latlng - FloatAttribute : 55.7278',
                'end_latlng - FloatAttribute : 55.727854', 'end_latlng - FloatAttribute : 55.82314',
                'end_latlng - FloatAttribute : 9.105082', 'end_latlng - Node',
                'external_id - StringAttribute : 0446b183956a4246b509e8178d962a73',
                'external_id - StringAttribute : 05a1170cb9421acf012cb660809f8707',
                'external_id - StringAttribute : 05c7eb647109b6c780272927a052d65d',
                'external_id - StringAttribute : 1a9455a9ebbc7a2c0bf0beea64daaa30',
                'external_id - StringAttribute : c28d5d8cb5f87f647b2c1fa8d3ffcd15',
                'external_id - StringAttribute : d991414cf07af9be57fbd0e74a89d8a4',
                'external_id - StringAttribute : dffe18b96bfe979f96633d7a21930813',
                'flagged - BoolAttribute : False', 'from_accepted_tag - BoolAttribute : False',
                'gear_id - Node', 'has_heartrate - BoolAttribute : False',
                'has_kudoed - BoolAttribute : False', 'heartrate_opt_out - BoolAttribute : False',
                'id - IntAttribute : 1853632245', 'id - IntAttribute : 1853676308',
                'id - IntAttribute : 1862269980', 'id - IntAttribute : 1866238587',
                'id - IntAttribute : 1870572749', 'id - IntAttribute : 1874410370',
                'id - IntAttribute : 1879752969', 'id - IntAttribute : 465645',
                'id - StringAttribute : a1853632245', 'id - StringAttribute : a1853676308',
                'id - StringAttribute : a1862269980', 'id - StringAttribute : a1866238587',
                'id - StringAttribute : a1870572749', 'id - StringAttribute : a1874410370',
                'id - StringAttribute : a1879752969', 'kudos_count - IntAttribute : 0',
                'kudos_count - IntAttribute : 1', 'kudos_count - IntAttribute : 2',
                'location_city - Node', 'location_country - StringAttribute : Denmark',
                'location_state - Node', 'manual - BoolAttribute : False', 'map - Node',
                'max_speed - FloatAttribute : 10.7', 'max_speed - FloatAttribute : 11.3',
                'max_speed - FloatAttribute : 14.0', 'max_speed - FloatAttribute : 4.0',
                'max_speed - FloatAttribute : 5.6', 'max_speed - FloatAttribute : 9.0',
                'max_speed - FloatAttribute : 9.4', 'moving_time - IntAttribute : 1143',
                'moving_time - IntAttribute : 1154', 'moving_time - IntAttribute : 1195',
                'moving_time - IntAttribute : 1406', 'moving_time - IntAttribute : 1514',
                'moving_time - IntAttribute : 2283', 'moving_time - IntAttribute : 777',
                'name - StringAttribute : 8 x ~30 sek interval med bakke',
                'name - StringAttribute : 8x30 sek interval',
                'name - StringAttribute : 9 x ~30 sek interval', 'name - StringAttribute : Evening Run',
                'name - StringAttribute : Løb med phillip', 'name - StringAttribute : Morgen',
                'name - StringAttribute : Morning Run', 'person__to__activities - Edge',
                'photo_count - IntAttribute : 0', 'pr_count - IntAttribute : 0',
                'pr_count - IntAttribute : 5', 'private - BoolAttribute : False',
                'private - BoolAttribute : True', 'resource_state - IntAttribute : 1',
                'resource_state - IntAttribute : 2',
                'start_date - DateTimeAttribute : 2018-09-12 15:09:44',
                'start_date - DateTimeAttribute : 2018-09-20 06:30:42',
                'start_date - DateTimeAttribute : 2018-09-24 07:45:02',
                'start_date - DateTimeAttribute : 2018-09-26 05:45:27',
                'start_date - DateTimeAttribute : 2018-09-28 08:59:08',
                'start_date - DateTimeAttribute : 2018-09-30 06:29:17',
                'start_date - DateTimeAttribute : 2018-10-02 16:16:49',
                'start_date_local - DateTimeAttribute : 2018-09-12 17:09:44',
                'start_date_local - DateTimeAttribute : 2018-09-20 08:30:42',
                'start_date_local - DateTimeAttribute : 2018-09-24 09:45:02',
                'start_date_local - DateTimeAttribute : 2018-09-26 07:45:27',
                'start_date_local - DateTimeAttribute : 2018-09-28 10:59:08',
                'start_date_local - DateTimeAttribute : 2018-09-30 08:29:17',
                'start_date_local - DateTimeAttribute : 2018-10-02 18:16:49',
                'start_latitude - FloatAttribute : 55.694375',
                'start_latitude - FloatAttribute : 55.727547',
                'start_latitude - FloatAttribute : 55.727747',
                'start_latitude - FloatAttribute : 55.727841',
                'start_latitude - FloatAttribute : 55.72792',
                'start_latitude - FloatAttribute : 55.727978',
                'start_latitude - FloatAttribute : 55.823333',
                'start_latlng - FloatAttribute : 12.57413', 'start_latlng - FloatAttribute : 12.574154',
                'start_latlng - FloatAttribute : 12.574233',
                'start_latlng - FloatAttribute : 12.574337',
                'start_latlng - FloatAttribute : 12.574341',
                'start_latlng - FloatAttribute : 12.586909',
                'start_latlng - FloatAttribute : 55.694375',
                'start_latlng - FloatAttribute : 55.727547',
                'start_latlng - FloatAttribute : 55.727747',
                'start_latlng - FloatAttribute : 55.727841', 'start_latlng - FloatAttribute : 55.72792',
                'start_latlng - FloatAttribute : 55.727978',
                'start_latlng - FloatAttribute : 55.823333', 'start_latlng - FloatAttribute : 9.105255',
                'start_latlng - Node', 'start_longitude - FloatAttribute : 12.57413',
                'start_longitude - FloatAttribute : 12.574154',
                'start_longitude - FloatAttribute : 12.574233',
                'start_longitude - FloatAttribute : 12.574337',
                'start_longitude - FloatAttribute : 12.574341',
                'start_longitude - FloatAttribute : 12.586909',
                'start_longitude - FloatAttribute : 9.105255',
                'summary_polyline - StringAttribute : _jcsIs|vkAy@jA~GEaC`b@d@dFjHJzD_DzHlAj@xIxCjHvCoA|AsF|Aj@qHqGfH`IcGmH',
                'summary_polyline - StringAttribute : chcsIi{vkApCh@gBl^T`B~@VCaBD|E~UbI`CfGnG|DfBYvAgGgKqL{OwAl@dFhHrA`@aG|@c@~I`Hq@`GeFzCwDwKeGs@{AkD}FZ',
                'summary_polyline - StringAttribute : kicsI}{vkAbD~@kBz[l@nCoAxFlFEvA`CbUuDvLjKnTd\\\\gFqG_EpH{KbDgG}HqNy@{Q_Hd@_[{E_D`FoAjAmHr@mSiD}@P}A',
                'summary_polyline - StringAttribute : ojcsIm{vkAvFKaChi@fYbH|EtIdCoBpD|BtAkEeKtEeBaAoBqHFqHxAOzDnEdAfHxAcDaJkIk\\\\TYcHfCg^sEiB',
                'summary_polyline - StringAttribute : yjcsIq|vkAjF`AsCdd@fG~CnKCe@fAlCaC{D~@lAIi@rAfAaB{BVxBc@aCXbCUuBZx@OQ|ApAgBsBXpBc@iI`AcJ}Ca@qB|@cBjBq]mDaB',
                'summary_polyline - StringAttribute : yx|rIckykAtE~GyA~GmK~U}WxObAbGkSje@nAnC{CvHTfChFxEdKhBxCcDpHwXqBmJyJWcRv[ZdCfFvE`LtAhCuD~GgX}CgKiIZwN|TvNbUmNiU{BzEdFrIrGxBfGsCbEqLz@uKsY|EI{EnR{d@EcGlPkI_dEj^',
                'timezone - StringAttribute : (GMT+01: 00) Europe/Copenhagen',
                'total_elevation_gain - FloatAttribute : 11.1',
                'total_elevation_gain - FloatAttribute : 13.2',
                'total_elevation_gain - FloatAttribute : 14.0',
                'total_elevation_gain - FloatAttribute : 22.0',
                'total_elevation_gain - FloatAttribute : 27.3',
                'total_elevation_gain - FloatAttribute : 27.7',
                'total_elevation_gain - FloatAttribute : 51.9', 'total_photo_count - IntAttribute : 0',
                'trainer - BoolAttribute : False', 'type - StringAttribute : Run',
                'upload_id - IntAttribute : 1986336755', 'upload_id - IntAttribute : 1986381489',
                'upload_id - IntAttribute : 1995341066', 'upload_id - IntAttribute : 1999406897',
                'upload_id - IntAttribute : 2003860523', 'upload_id - IntAttribute : 2007831642',
                'upload_id - IntAttribute : 2013405598', 'utc_offset - FloatAttribute : 7200.0',
                'visibility - StringAttribute : everyone', 'visibility - StringAttribute : only_me',
                'workout_type - IntAttribute : 0', 'workout_type - IntAttribute : 3']

    @staticmethod
    def open_m_health():
        return ['body-temperature - Node', 'body-temperature__to__body-temperature - Edge',
                'body-temperature__to__effective_time_frame - Edge',
                'body_temperature - IntAttribute : 97',
                'date_time - DateTimeAttribute : 2013-02-05 07:25:00+00:00',
                'effective_time_frame - Node', 'measurement_location - StringAttribute : forehead',
                'person__to__body-temperature - Edge']

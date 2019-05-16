import django
from django.test import TransactionTestCase

from MetaDataApi.metadata.models import Object


class TestObjectTableView(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestObjectTableView, cls).setUpClass()
        django.setup()

    def setUp(self):
        from MetaDataApi.metadata.tests import LoadTestData
        LoadTestData.init_strava_schema_from_file()
        LoadTestData.init_strava_data_from_file()
        obj = Object.objects.get(label="activities")
        from MetaDataApi.metadata.models.meta.object_table_view import ObjectTableView
        self.table_view = ObjectTableView(obj, max_number_of_atts=9)

    def test_attribute_labels_are_generated_correctly(self):
        att_labels = self.table_view.get_selected_attribute_labels()

        excpected_att_labels = ['resource_state', 'name', 'distance', 'moving_time', 'elapsed_time',
                                'total_elevation_gain', 'type', 'workout_type', 'id']

        self.assertListEqual(excpected_att_labels, att_labels)

    def test_values_are_correct(self):
        att_inst_values = self.table_view.get_selected_object_instance_attributes()

        excpected_att_values = [
            ['2', 'Evening Run', '3503.7', '1143', '1848', '27.3', 'Run', '0', '1879752969', ],
            ['2', '9 x ~30 sek interval', '3133.3', '777', '1257', '11.1', 'Run', '3', '1874410370', ],
            ['2', '8 x ~30 sek interval med bakke', '3555.6', '1154', '1821', '14.0', 'Run', '3', '1870572749', ],
            ['2', '8x30 sek interval', '3926.8', '1195', '1765', '27.7', 'Run', '3', '1866238587', ],
            ['2', 'Morning Run', '4774.5', '1514', '1695', '13.2', 'Run', '0', '1862269980', ],
            ['2', 'Morgen', '4395.6', '1406', '2149', '22.0', 'Run', '0', '1853676308', ],
            ['2', 'Løb med phillip', '11867.8', '2283', '660103', '51.9', 'Run', '0', '1853632245', ],
            ['2', 'Evening Run', '3503.7', '1143', '1848', '27.3', 'Run', '0', '1879752969', ],
            ['2', '9 x ~30 sek interval', '3133.3', '777', '1257', '11.1', 'Run', '3', '1874410370', ],
            ['2', '8 x ~30 sek interval med bakke', '3555.6', '1154', '1821', '14.0', 'Run', '3', '1870572749', ],
            ['2', '8x30 sek interval', '3926.8', '1195', '1765', '27.7', 'Run', '3', '1866238587', ],
            ['2', 'Morning Run', '4774.5', '1514', '1695', '13.2', 'Run', '0', '1862269980', ],
            ['2', 'Morgen', '4395.6', '1406', '2149', '22.0', 'Run', '0', '1853676308', ],
            ['2', 'Løb med phillip', '11867.8', '2283', '660103', '51.9', 'Run', '0', '1853632245', ]]

        att_inst_values.sort(key=lambda x: x[3])
        excpected_att_values.sort(key=lambda x: x[3])

        self.assertListEqual(excpected_att_values, att_inst_values)

from unittest.mock import patch

import django
from django.test import TransactionTestCase
from model_bakery import baker
from parameterized import parameterized

from MetaDataApi.tests.utils_for_testing.utils_for_testing import get_method_path
from MetaDataApi.utils import JsonUtils
from MetaDataApi.utils.django_model_utils import django_file_utils
from MetaDataApi.utils.django_model_utils.django_file_utils import FileType
from dataproviders import tasks
from dataproviders.models import DataFetch, DataFileUpload
from dataproviders.services.transform_files_to_data import clean_data_from_data_file, clean_invalid_key_chars


class TestTransformFilesToData(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestTransformFilesToData, cls).setUpClass()
        django.setup()

    def test_transform_json_file(self):
        json_file = self.build_json_file()
        result = clean_data_from_data_file(json_file)
        result = JsonUtils.validate(result)
        expected = {'quiz': {'sport': {'q1': {'question': 'Which one is correct team name in NBA?',
                                              'options': ['New York Bulls', 'Los Angeles Kings',
                                                          'Golden State Warriros', 'Huston Rocket'],
                                              'answer': 'Huston Rocket'}}, 'maths': {
            'q1': {'question': '5 + 7 = ?', 'options': ['10', '11', '12', '13'], 'answer': '12'},
            'q2': {'question': '12 - 8 = ?', 'options': ['1', '2', '3', '4'], 'answer': '4'}}}}
        self.assertEqual(result, expected)

    def test_transform_csv_file(self):
        file = django_file_utils.convert_str_to_file(self.dummy_csv_string(), filetype=FileType.CSV)
        result = clean_data_from_data_file(file)
        result = JsonUtils.validate(result)
        expected = self.dummy_csv_data_structure()
        self.assertEqual(result, expected)

    def test_transform_zip_with_csv(self):
        csv_file = self.dummy_csv_string()
        file = django_file_utils.create_django_zip_file({"csv1.csv": csv_file})
        result = clean_data_from_data_file(file)
        expected = {'csv1': self.dummy_csv_data_structure()}
        self.assertEqual(result, expected)

    def build_csv_file(self):
        return django_file_utils.convert_str_to_file(self.dummy_csv_string(), filetype=FileType.CSV)

    def test_transform_zip_with_json(self):
        json_file = self.dummy_json_string()
        file = django_file_utils.create_django_zip_file({"json1.json": json_file})
        result = clean_data_from_data_file(file)
        expected = {'json1': self.dummy_json_data_structure()}
        self.assertEqual(result, expected)

    def test_transform_zip_with_json_and_csv(self):
        csv_file = self.dummy_csv_string()
        json_file = self.dummy_json_string()
        file = django_file_utils.create_django_zip_file({"json1.json": json_file, "csv1.csv": csv_file})
        result = clean_data_from_data_file(file)
        expected = {'json1': self.dummy_json_data_structure(), 'csv1': self.dummy_csv_data_structure()}
        self.assertEqual(result, expected)

    @parameterized.expand([
        ["true", True],
        ["false", False],
    ])
    def test_execute_on_save_methods_when_has_been_refined(self, name, has_been_refined):
        with patch(get_method_path(tasks.clean_data_from_source) + ".delay") as mock_method:
            baker.make(DataFetch.__name__, make_m2m=True, has_been_refined=has_been_refined)
        self.assertEqual(mock_method.call_count, int(not has_been_refined))

    def test_transform_on_real_files(self):
        local_file_path = 'dataproviders/tests/services/test_files/journey-test1.zip'
        data_file = django_file_utils.create_django_file_from_local(local_file_path)
        # provider = baker.make(DataProvider.__name__, make_m2m=True)
        # user = baker.make(User.__name__)
        # dfu = DataFileUpload(data_provider=provider, user=user)
        # dfu.data_file_from_source.save("journey-test1.zip", data_file, save=True)
        dfu = baker.make(DataFileUpload.__name__, make_m2m=True, data_file_from_source=data_file,
                         has_been_refined=False)
        dfu.refresh_from_db()
        self.assertIsNotNone(dfu.refined_data_file)
        file_data = dfu.refined_data_file.data_file.read()
        file_content = JsonUtils.loads(file_data.decode())
        expected = {'text': '<p dir="auto">Rimelig driven.</p>', 'date_modified': 1579414106050,
                    'date_journal': 1579414071717, 'id': '1579414071512-3fd9d6575f3b10ea',
                    'preview_text': '<p dir="auto">Rimelig driven.</p>',
                    'address': 'Lagesminde Allé 1A, 2660 Brøndby Strand, Denmark', 'music_artist': '',
                    'music_title': '', 'lat': 55.6175898, 'lon': 12.4346179, 'mood': 1, 'label': '', 'folder': '',
                    'sentiment': 1.25, 'timezone': 'Europe/Copenhagen', 'favourite': False, 'type': 'html',
                    'weather': {'id': 0, 'degree_c': 1.9, 'description': 'Scattered clouds', 'icon': '02n',
                                'place': 'Brøndbyvester'}, 'photos': [], 'tags': []}
        self.assertEqual(next(iter(file_content.values())), expected)

    def test_clean_invalid_key_chars(self):
        data = self.dummy_json_data_structure()
        data["quiz$$"] = data.pop("quiz")
        data["quiz$$"]["sport"]["q1%%"] = data["quiz$$"]["sport"].pop("q1")
        data["quiz$$"]["sport"]["q1%%"]["questio@@n"] = data["quiz$$"]["sport"]["q1%%"].pop("question")
        res = clean_invalid_key_chars(data)
        expected = {'quizXX': {'sport': {'q1XX': {'questioXXn': 'Which one is correct team name in NBA?',
                                                  'options': ['New York Bulls', 'Los Angeles Kings',
                                                              'Golden State Warriros', 'Huston Rocket'],
                                                  'answer': 'Huston Rocket'}}, 'maths': {
            'q1': {'question': '5 + 7 = ?', 'options': ['10', '11', '12', '13'], 'answer': '12'},
            'q2': {'question': '12 - 8 = ?', 'options': ['1', '2', '3', '4'], 'answer': '4'}}}}
        self.assertEqual(res, expected)

    def build_json_file(self):
        return django_file_utils.convert_str_to_file(self.dummy_json_string(), filetype=FileType.JSON)

    def dummy_json_string(self):
        return JsonUtils.dumps(self.dummy_json_data_structure())

    def dummy_csv_string(self):
        return '"Name",     "Sex", "Age", "Height (in)", "Weight (lbs)" \n \
                "Alex",       "M",   41,       74,      170 \n \
                "Bert",       "M",   42,       68,      166'

    def dummy_csv_data_structure(self):
        return [{'Name': '                 "Alex"', '     "Sex"': '       "M"', ' "Age"': '   41',
                 ' "Height (in)"': '       74', ' "Weight (lbs)" ': '      170 '},
                {'Name': '                 "Bert"', '     "Sex"': '       "M"', ' "Age"': '   42',
                 ' "Height (in)"': '       68', ' "Weight (lbs)" ': '      166'}]

    def dummy_json_data_structure(self):
        return {
            "quiz": {
                "sport": {
                    "q1": {
                        "question": "Which one is correct team name in NBA?",
                        "options": [
                            "New York Bulls",
                            "Los Angeles Kings",
                            "Golden State Warriros",
                            "Huston Rocket"
                        ],
                        "answer": "Huston Rocket"
                    }
                },
                "maths": {
                    "q1": {
                        "question": "5 + 7 = ?",
                        "options": [
                            "10",
                            "11",
                            "12",
                            "13"
                        ],
                        "answer": "12"
                    },
                    "q2": {
                        "question": "12 - 8 = ?",
                        "options": [
                            "1",
                            "2",
                            "3",
                            "4"
                        ],
                        "answer": "4"
                    }
                }
            }
        }

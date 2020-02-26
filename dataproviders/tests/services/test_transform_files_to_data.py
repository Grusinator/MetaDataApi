from unittest.mock import patch

import django
from django.test import TransactionTestCase
from model_bakery import baker
from parameterized import parameterized

from MetaDataApi.utils import JsonUtils
from MetaDataApi.utils.django_utils import django_file_utils
from MetaDataApi.utils.django_utils.django_file_utils import FileType
from MetaDataApi.utils.unittest_utils.unittest_utils import get_method_path
from dataproviders import tasks
from dataproviders.models import DataFetch
from dataproviders.services.transform_files_to_data import TransformFilesToData
from dataproviders.services.transform_files_to_data.transform_methods import clean_key_value_strings


class TestTransformFilesToData(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestTransformFilesToData, cls).setUpClass()
        django.setup()

    def test_transform_json_file(self):
        json_file = self.build_json_file()
        result = TransformFilesToData().clean_data_from_file(json_file)
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
        result = TransformFilesToData().clean_data_from_file(file)
        result = JsonUtils.validate(result)
        expected = [{'Name': '"Alex"', 'Sex': '"M"', 'Age': '41', 'Height_in': '74', 'Weight_lbs': '170'},
                    {'Name': '"Bert"', 'Sex': '"M"', 'Age': '42', 'Height_in': '68', 'Weight_lbs': '166'}]
        self.assertEqual(result, expected)

    def test_transform_zip_with_csv(self):
        csv_file = self.dummy_csv_string()
        file = django_file_utils.create_django_zip_file({"csv1.csv": csv_file})
        result = TransformFilesToData().clean_data_from_file(file)
        expected = {'csv1': [{'Name': '"Alex"', 'Sex': '"M"', 'Age': '41', 'Height_in': '74', 'Weight_lbs': '170'},
                             {'Name': '"Bert"', 'Sex': '"M"', 'Age': '42', 'Height_in': '68', 'Weight_lbs': '166'}]}
        self.assertEqual(result, expected)

    def build_csv_file(self):
        return django_file_utils.convert_str_to_file(self.dummy_csv_string(), filetype=FileType.CSV)

    def test_transform_zip_with_json(self):
        json_file = self.dummy_json_string()
        file = django_file_utils.create_django_zip_file({"json1.json": json_file})
        result = TransformFilesToData().clean_data_from_file(file)
        expected = {'json1': self.dummy_json_data_structure()}
        self.assertEqual(result, expected)

    def test_transform_zip_with_json_and_csv(self):
        csv_file = self.dummy_csv_string()
        json_file = self.dummy_json_string()
        file = django_file_utils.create_django_zip_file({"json1.json": json_file, "csv1.csv": csv_file})
        result = TransformFilesToData().clean_data_from_file(file)
        expected = {'json1': {'quiz': {'sport': {'q1': {'question': 'Which one is correct team name in NBA?',
                                                        'options': ['New York Bulls', 'Los Angeles Kings',
                                                                    'Golden State Warriros', 'Huston Rocket'],
                                                        'answer': 'Huston Rocket'}}, 'maths': {
            'q1': {'question': '5 + 7 = ?', 'options': ['10', '11', '12', '13'], 'answer': '12'},
            'q2': {'question': '12 - 8 = ?', 'options': ['1', '2', '3', '4'], 'answer': '4'}}}},
                    'csv1': [{'Name': '"Alex"', 'Sex': '"M"', 'Age': '41', 'Height_in': '74', 'Weight_lbs': '170'},
                             {'Name': '"Bert"', 'Sex': '"M"', 'Age': '42', 'Height_in': '68', 'Weight_lbs': '166'}]}
        self.assertEqual(result, expected)

    @parameterized.expand([
        ["true", True],
        ["false", False],
    ])
    def test_execute_on_save_methods_when_has_been_refined(self, name, has_been_refined):
        with patch(get_method_path(tasks.clean_data_from_source) + ".delay") as mock_method:
            baker.make(DataFetch.__name__, make_m2m=True, has_been_refined=has_been_refined)
        self.assertEqual(mock_method.call_count, int(not has_been_refined))

    def test_clean_invalid_key_chars(self):
        data = self.dummy_json_data_structure()
        data["quiz$$"] = data.pop("quiz")
        data["quiz$$"]["sport"]["q1%%"] = data["quiz$$"]["sport"].pop("q1")
        data["quiz$$"]["sport"]["q1%%"]["questio@@n"] = data["quiz$$"]["sport"]["q1%%"].pop("question")
        res = clean_key_value_strings(data)
        expected = {'quiz': {'sport': {
            'q1': {'options': ['New York Bulls', 'Los Angeles Kings', 'Golden State Warriros', 'Huston Rocket'],
                   'answer': 'Huston Rocket', 'question': 'Which one is correct team name in NBA?'}}, 'maths': {
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

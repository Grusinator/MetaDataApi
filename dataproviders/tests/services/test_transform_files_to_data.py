import django
from django.test import TransactionTestCase

from MetaDataApi.utils import JsonUtils
from MetaDataApi.utils.django_model_utils import django_file_utils
from MetaDataApi.utils.django_model_utils.django_file_utils import FileType
from dataproviders.services.transform_files_to_data import transform_data_file


class TestTransformFilesToData(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestTransformFilesToData, cls).setUpClass()
        django.setup()

    def test_transform_json_file(self):
        json_file = self.build_json_file()
        result = transform_data_file(json_file)
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
        result = transform_data_file(file)
        result = JsonUtils.validate(result)
        expected = [{'Name': '                 "Alex"', '     "Sex"': '       "M"', ' "Age"': '   41',
                     ' "Height (in)"': '       74', ' "Weight (lbs)" ': '      170 '},
                    {'Name': '                 "Bert"', '     "Sex"': '       "M"', ' "Age"': '   42',
                     ' "Height (in)"': '       68', ' "Weight (lbs)" ': '      166'}]
        self.assertEqual(result, expected)

    def test_transform_zip_with_csv(self):
        csv_file = self.build_csv_file()
        file = django_file_utils.create_django_zip_file({"csv1.csv": csv_file})
        result = transform_data_file(file)
        result = JsonUtils.validate(result)
        expected = {

        }
        self.assertEqual(result, expected)

    def build_csv_file(self):
        return django_file_utils.convert_str_to_file(self.dummy_csv_string(), filetype=FileType.CSV)

    def test_transform_zip_with_json(self):
        json_file = self.dummy_json_string()
        file = django_file_utils.create_django_zip_file({"json1.json": json_file})
        result = transform_data_file(file)
        result = JsonUtils.validate(result)
        expected = {

        }
        self.assertEqual(result, expected)

    def test_transform_zip_with_json_and_csv(self):
        csv_file = self.dummy_csv_string()
        json_file = self.dummy_json_string()
        file = django_file_utils.create_django_zip_file({"json1.json": json_file, "csv1.csv": csv_file})
        result = transform_data_file(file)
        expected = {

        }
        self.assertEqual(result, expected)

    def build_json_file(self):
        return django_file_utils.convert_str_to_file(self.dummy_json_string(), filetype=FileType.JSON)

    def dummy_csv_string(self):
        return '"Name",     "Sex", "Age", "Height (in)", "Weight (lbs)" \n \
                "Alex",       "M",   41,       74,      170 \n \
                "Bert",       "M",   42,       68,      166'

    def dummy_json_string(self):
        return JsonUtils.dumps({
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
        })

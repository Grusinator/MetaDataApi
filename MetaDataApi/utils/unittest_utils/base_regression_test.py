import os
from unittest import TestCase

from MetaDataApi.utils import JsonType, JsonUtils


class BaseRegressionTest(TestCase):
    test_data_path = "./tests/test_data"
    test_data_results_path = "./tests/test_data_results"

    def build_test_file_path(self, file):
        return os.path.join(self.test_data_path, file)

    def get_data_from_file(self, filename):
        test_file_path = self.build_test_file_path(filename)
        return self.try_read_json_file(test_file_path)

    def try_read_json_file(self, filename):
        try:
            JsonUtils.read_json_file(filename)
        except FileNotFoundError:
            pass

    def get_file(self, filename):
        test_file_path = self.build_test_file_path(filename)
        return open(test_file_path)

    def assert_result_equals_expected_json(self, result: JsonType, input_filename):
        expected = self.try_get_result_data_or_create_it(input_filename, result)
        self.assert_data_equal(expected, result)

    def try_get_result_data_or_create_it(self, input_filename, result_data):
        result_file_path = self.build_result_file_path(input_filename)
        try:
            return JsonUtils.read_json_file(result_file_path)
        except FileNotFoundError:
            JsonUtils.write_to_file(result_data, result_file_path)
            raise FileNotFoundError(f"Expected result did not exists before but has now been created, "
                                    f"check the file {result_file_path} to ensure the result is correct", )

    def build_result_file_path(self, input_file):
        file_name = os.path.splitext(input_file)[0]
        result_filename = f"{file_name}_results.json"
        test_data_results_file = os.path.join(self.test_data_results_path, result_filename)
        return test_data_results_file

    def assert_data_equal(self, expected, result):
        if isinstance(expected, list):
            self.assertListEqual(result, expected)
        elif isinstance(expected, dict):
            self.assertDictEqual(result, expected)
        else:
            self.assertEqual(result, expected)

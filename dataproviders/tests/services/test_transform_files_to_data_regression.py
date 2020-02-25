import os

import django
from django.test import TransactionTestCase
from model_bakery import baker

from MetaDataApi.utils import JsonUtils
from MetaDataApi.utils.django_utils import django_file_utils
from MetaDataApi.utils.unittest_utils.base_regression_test import BaseRegressionTest
from dataproviders.models import DataFileUpload


class TestTransformFilesToData(TransactionTestCase, BaseRegressionTest):
    test_data_path = 'dataproviders/tests/services/test_data/test_files'
    test_data_results_path = 'dataproviders/tests/services/test_data/expected_result'
    exclude = ("samsunghealth_201809301847.zip",)

    @classmethod
    def setUpClass(cls):
        super(TestTransformFilesToData, cls).setUpClass()
        django.setup()

    def test_run_specific_test(self):
        file = "com.samsung.health.exercise.201809301847.csv"
        self.run_regression_test_on_file(file)

    def test_all_files(self):
        for file in os.listdir(self.test_data_path):
            if file in self.exclude:
                continue
            with self.subTest(msg=file):
                self.run_regression_test_on_file(file)

    def run_regression_test_on_file(self, file):
        file_path = self.build_test_file_path(file)
        data_file = django_file_utils.create_django_file_from_local(file_path)
        dfu = baker.make(DataFileUpload.__name__, make_m2m=True, data_file_from_source=data_file,
                         has_been_refined=False)
        dfu.refresh_from_db()
        self.assertIsNotNone(dfu.refined_data_file)
        file_data = dfu.refined_data_file.data_file.read()
        file_content = JsonUtils.loads(file_data.decode())

        self.assert_result_equals_expected_json(file_content, file)

import django
from django.test import TransactionTestCase
from parameterized import parameterized

from dataproviders.services.transform_files_to_data.transform_methods.infer_object_name import \
    infer_object_name_from_path


class TestInferObjectName(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()

    @parameterized.expand([
        ["/some/long/path-32947274324.json", "some_long_path"],
        ["/some/long-example-8329928347/path-32947274324.json", "some_long_example_path"],
    ])
    def test_infer_object_name_from_path(self, input, output):
        res = infer_object_name_from_path(input)
        self.assertEqual(res, output)

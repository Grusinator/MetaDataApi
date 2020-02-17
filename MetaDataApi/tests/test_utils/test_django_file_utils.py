import django
from django.core.files.base import ContentFile
from django.test import TransactionTestCase

from MetaDataApi.utils.django_utils.django_file_utils import create_django_zip_file, unzip_django_zipfile, \
    convert_file_to_str


class TestDjangoFileUtils(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDjangoFileUtils, cls).setUpClass()
        django.setup()

    def test_create_zip_file(self):
        files = {"file1.json": '{"name: "john"}'}
        zipfile = create_django_zip_file(files)
        self.assertIsInstance(zipfile, ContentFile)

    def test_read_zipfile(self):
        files = {"file1.json": '{"name: "john"}'}
        zipfile = create_django_zip_file(files)
        data = unzip_django_zipfile(zipfile)
        data["file1.json"] = convert_file_to_str(data["file1.json"])
        self.assertEqual(data, files)

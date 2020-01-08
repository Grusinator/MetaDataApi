# Create your tests here.
import django
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from MetaDataApi.utils import DjangoModelUtils, JsonUtils
from dataproviders.models import DataDump, DataProviderUser, DataProvider, Endpoint
from dataproviders.services import InitializeDataProviders
from dataproviders.tests.mock_objects.mock_data_dump import data_dump_json_strava_activity
from dynamic_models.tasks import build_models_from_data_dump


class TestRunTasks(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()
        InitializeDataProviders.load()

    def test_build_data_from_dump(self):
        user = User.objects.create(username="test1")
        dp = DataProvider.objects.get(provider_name="strava")
        DataProviderUser.objects.create(data_provider=dp, user=user)
        endpoint = Endpoint.objects.get(data_provider=dp, endpoint_name="activity")
        data = data_dump_json_strava_activity()
        data_str = JsonUtils.dumps(data)
        file = DjangoModelUtils.convert_str_to_file(data_str, filetype=DjangoModelUtils.FileType.JSON)
        data_dump = DataDump.objects.create(endpoint=endpoint, file=file, user=user)
        build_models_from_data_dump(data_dump.pk)

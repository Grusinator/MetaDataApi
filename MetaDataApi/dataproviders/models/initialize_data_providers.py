import json
import logging

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import DataProviderO
from MetaDataApi.metadata.utils import JsonUtils

logger = logging.getLogger(__name__)

class InitializeDataProviders:
    local_client_file = "data_providers.json"

    @classmethod
    def load_client_ids_and_secrets(cls):
        # TODO try or AWS
        return JsonUtils.read_json_file(cls.local_client_file)

    @staticmethod
    def get_default_data_providers():
        return [
            DataProvider(
                provider_name="endomondo",
                api_type="Oauth2-rest",
                api_endpoint="https://api.endomondo.com/api/1/",
                authorize_url="https://www.endomondo.com/oauth/authorize",
                access_token_url="https://api.endomondo.com/oauth/access_token",
                scope=json.dumps([]),
                rest_endpoints_list=json.dumps([]),
                json_schema_file_url=""
            ),
            DataProvider(
                provider_name="withings",
                api_type="Oauth2-rest",
                api_endpoint="https://wbsapi.withings.net/",
                authorize_url="https://account.withings.com/oauth2_user/authorize2",
                access_token_url="https://account.withings.com/oauth2/token",
                scope=json.dumps([
                    # issues with multiple scopes for some reason, but first when i log in
                    # "user.info",
                    # "user.metrics",
                    "user.activity"
                ]),
                rest_endpoints_list=json.dumps([
                    # "v2/user?action=getdevice",
                    # "measure?action=getmeas",
                    {"name": "sleep",
                     "url": "v2/sleep?action=getsummary&access_token={AuthToken:}&startdateymd={StartDateTime:Y-M-d}&enddateymd={EndDateTime:Y-M-d}"},
                    {"name": "athlete",
                     "url": "v2/sleep?action=get&access_token={AuthToken:}&startdate={StartDateTime:UTCSEC}&enddate={EndDateTime:UTCSEC}"},
                ]),
                json_schema_file_url=""
            ),
            DataProvider(
                provider_name="strava",
                api_type="Oauth2-rest",
                api_endpoint="https://www.strava.com/api/",
                authorize_url="https://www.strava.com/oauth/authorize",
                access_token_url="https://www.strava.com/oauth/token",
                scope=json.dumps(["view_private"]),
                rest_endpoints_list=json.dumps([
                    {"name": "activity", "url": "v3/activities"},
                    {"name": "zone", "url": "v3/athlete/zones"},
                    {"name": "athlete", "url": "v3/athlete"},
                ]),
                json_schema_file_url=""
            ),
            DataProvider(
                provider_name="oura",
                api_type="Oauth2-rest",
                api_endpoint="https://api.ouraring.com/",
                authorize_url="https://cloud.ouraring.com/oauth/authorize",
                access_token_url="https://api.ouraring.com/oauth/token",
                scope=json.dumps([
                    "email",
                    "personal",
                    "daily"]),
                rest_endpoints_list=json.dumps([
                    {"name": "user_info", "url": "v1/userinfo"},
                    {"name": "sleep", "url": "v1/sleep?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}"},
                    {"name": "activity", "url": "v1/activity?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}"},
                    {"name": "readiness", "url": "v1/readiness?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}"}
                ]),
                json_schema_file_url=""
            ),
            DataProvider(
                provider_name="google_fit",
                api_endpoint="https://www.googleapis.com/fitness/",
                authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
                access_token_url="https://www.googleapis.com/oauth2/v4/token",
                scope=json.dumps([
                    "https://www.googleapis.com/auth/fitness.activity.read",
                ]),
                rest_endpoints_list=json.dumps([
                    {"name": "data_source", "url": "v1/users/me/dataSources"},
                ]),
                json_schema_file_url=""
            ),
            DataProvider(
                provider_name="google_drive",
                api_endpoint="",
                authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
                access_token_url="https://www.googleapis.com/oauth2/v4/token",
                scope=json.dumps([
                    "https://www.googleapis.com/auth/drive",  # full access, change later
                ]),
                rest_endpoints_list=json.dumps([]),
                json_schema_file_url="https://www.googleapis.com/discovery/v1/apis/drive/v3/rest"
            ),
            DataProvider(
                provider_name="rescue_time",
                api_endpoint="",
                authorize_url="",
                access_token_url="",
                client_id="",
                client_secret="",
                scope=json.dumps([]),
                rest_endpoints_list=json.dumps([]),
                json_schema_file_url=""
            ),
            DataProvider(
                provider_name="polar",
                api_endpoint="https://www.polaraccesslink.com/",
                authorize_url="https://flow.polar.com/oauth2/authorization",
                access_token_url="https://polarremote.com/v2/oauth2/token",
                scope=json.dumps([]),
                rest_endpoints_list=json.dumps([{"name": "notifications", "url": "/v3/notifications"}]),
                json_schema_file_url=""
            ),
            DataProvider(
                provider_name="facebook",
                api_endpoint="",
                authorize_url="",
                access_token_url="",
                scope=json.dumps([]),
                rest_endpoints_list=json.dumps([]),
                json_schema_file_url=""
            ),
            DataProvider(
                provider_name="spotify",
                api_endpoint="https://api.spotify.com/",
                authorize_url="https://accounts.spotify.com/authorize",
                access_token_url="https://accounts.spotify.com/api/token",
                scope=json.dumps(["user-read-recently-played"]),
                rest_endpoints_list=json.dumps([{"name": "recently_played", "url": "v1/me/player/recently-played"}]),
                json_schema_file_url=""
            ),
            DataProvider(
                provider_name="template",
                api_endpoint="",
                authorize_url="",
                access_token_url="",
                scope=json.dumps([]),
                rest_endpoints_list=json.dumps([]),
                json_schema_file_url=""
            ),
        ]

    @classmethod
    def load(cls):
        for data_provider in cls.get_default_data_providers():
            if DataProvider.exists(data_provider.provider_name):
                cls.update_values(data_provider)
            else:
                data_provider.save()

    @classmethod
    def load_from_json(cls):
        providers = cls.load_client_ids_and_secrets()
        [cls.try_create_provider(provider) for provider in providers]

    @classmethod
    def try_create_provider(cls, provider: dict):
        try:
            DataProviderO(json_object=provider)
        except Exception as e:
            logger.error("error durring loading of dataprovider %s" % provider["provider_name"])


    @classmethod
    def update_values(cls, data_provider):
        existing_dp = DataProvider.objects.filter(provider_name=data_provider.provider_name)
        existing_dp.update(
            api_endpoint=data_provider.api_endpoint,
            authorize_url=data_provider.authorize_url,
            access_token_url=data_provider.access_token_url,
            client_id=data_provider.client_id,
            client_secret=data_provider.client_secret,
            scope=data_provider.scope,
            rest_endpoints_list=data_provider.rest_endpoints_list,
            json_schema_file_url=data_provider.json_schema_file_url
        )

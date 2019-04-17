import json

from MetaDataApi.dataproviders.models import DataProvider


class InitializeDataProviders:

    @staticmethod
    def get_default_data_providers():
        return [
            DataProvider(
                provider_name="endomondo",
                api_type="Oauth2-rest",
                api_endpoint="https://api.endomondo.com/api/1/",
                authorize_url="https://www.endomondo.com/oauth/authorize",
                access_token_url="https://api.endomondo.com/oauth/access_token",
                client_id="",
                client_secret="",
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
                client_id="a80378abe1059ef7c415cf79b09b1270f828c4a0fbfdc52dbec06ae5f71b4bb6",
                client_secret="1f1d852451385469a56ef6494cbd2e94c07421c3ee5ffbfca63216079fd36d1a",
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
                client_id="28148",
                client_secret="ed5f469f798830c7214fc8efad54790799fc3ae1",
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
                client_id="Q43N7PFF2RI3SF52",
                client_secret="CX6MEERKWUBIMBMRZOVY6BAAQLF5KDDL",
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
                client_id="166351402500-m9302qf47ua66qbr1gdbgrronssnm2v2.apps.googleusercontent.com",
                client_secret="W_jKUZmRCGl05G-TMYuFPbjY",
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
                client_id="166351402500-m9302qf47ua66qbr1gdbgrronssnm2v2.apps.googleusercontent.com",
                client_secret="W_jKUZmRCGl05G-TMYuFPbjY",
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
                provider_name="template",
                api_endpoint="",
                authorize_url="",
                access_token_url="",
                client_id="",
                client_secret="",
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

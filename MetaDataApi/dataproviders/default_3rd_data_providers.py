from MetaDataApi.users.models import ThirdPartyDataProvider

default_data_providers = [
    ThirdPartyDataProvider(
        name="dummy",
        api_endpoint="",
        authorize_url="",
        access_token_url="",
        client_id="",
        client_secret="",
        scope="",
        redirect_url="",
        rest_endpoints_list="",
        json_schema_file_url=""
    ),
    ThirdPartyDataProvider(
        name="Endomondo",
        api_endpoint="https://api.endomondo.com/api/1/",
        authorize_url="https://www.endomondo.com/oauth/authorize",
        access_token_url="https://api.endomondo.com/oauth/access_token",
        client_id="",
        client_secret="",
        scope="",
        redirect_url="",
        rest_endpoints_list="",
        json_schema_file_url=""
    ),
    ThirdPartyDataProvider(
        name="Nokia",
        api_endpoint="",
        authorize_url="https://account.health.nokia.com/oauth2_user/authorize2",
        access_token_url="https://account.health.nokia.com/oauth2/token",
        client_id="a80378abe1059ef7c415cf79b09b1270f828c4a0fbfdc52dbec06ae5f71b4bb6",
        client_secret="1f1d852451385469a56ef6494cbd2e94c07421c3ee5ffbfca63216079fd36d1a",
        scope="user.info",
        redirect_url="http://localhost:/oauth2redirect",
        rest_endpoints_list="",
        json_schema_file_url=""
    ),
    ThirdPartyDataProvider(
        name="Strava",
        api_endpoint="https://www.strava.com/api/v3/",
        authorize_url="https://www.strava.com/oauth/authorize",
        access_token_url="https://www.strava.com/oauth/token",
        client_id="28148",
        client_secret="ed5f469f798830c7214fc8efad54790799fc3ae1",
        scope="view_private",
        redirect_url="http://localhost:/oauth2redirect",
        rest_endpoints_list="",
        json_schema_file_url=""
    ),
]

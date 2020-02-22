from dataproviders.models.ApiTypes import ApiTypes


class MockDataProvider:

    @classmethod
    def build_full_data(cls):
        return {
            **cls.build_base_data(),
            **cls.build_http_data(),
            **cls.build_oauth_data(),
            **cls.build_endpoints_data()
        }

    @classmethod
    def build_base_with_http_data(cls):
        return {**cls.build_base_data(), **cls.build_http_data()}

    @classmethod
    def build_base_with_oauth_data(cls):
        return {**cls.build_base_data(), **cls.build_oauth_data()}

    @classmethod
    def build_base_with_endpoints_data(cls):
        return {**cls.build_base_data(), **cls.build_endpoints_data()}

    @classmethod
    def build_base_data(cls):
        return {
            'provider_name': 'dsfsd4',
            'api_type': ApiTypes.OAUTH_GRAPHQL.value,
            'api_endpoint': '56',
        }

    @classmethod
    def build_oauth_data(cls):
        return {
            "oauth_config": {
                "authorize_url": "https://account.withings.com/oauth2_user/authorize2",
                "access_token_url": "https://account.withings.com/oauth2/token",
                "client_id": "123",
                "client_secret": "12345",
                "scope": ["user.activity"]
            }
        }

    @classmethod
    def build_http_data(cls):
        return {
            "http_config": {
                "header": {
                    "User-Agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
                    "X-Auth-Token": "{AuthToken:}",
                    "Content-Type": "application/json"
                },
                "url_encoded_params": {
                    "d": "a",
                    "c": "t"
                },
            }
        }

    @classmethod
    def build_endpoints_data(cls):
        return {
            'endpoints': [
                {'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET'},
                {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET'}
            ]
        }

    @classmethod
    def build_strava_data_provider_json(cls):
        return {
            "provider_name": "strava",
            "api_endpoint": "https://www.strava.com/api/",
            "oauth_config": {
                "authorize_url": "https://www.strava.com/oauth/authorize",
                "access_token_url": "https://www.strava.com/oauth/token",
                "client_id": "28148",
                "client_secret": "ed5f469f798830c7214fc8efad54790799fc3ae1",
                "scope": [
                    "view_private"
                ]
            },
            "endpoints": [
                {
                    "api_type": "OauthRest",
                    "endpoint_name": "activity",
                    "endpoint_url": "v3/activities",
                    "data_fetches": [
                        {
                            "date_downloaded": "20102019",
                        }
                    ]
                },
                {
                    "api_type": "OauthRest",
                    "endpoint_name": "zone",
                    "endpoint_url": "v3/athlete/zones",
                    "data_fetches": [
                        {
                            "date_downloaded": "21102019",
                        }
                    ]
                },
                {
                    "api_type": "OauthRest",
                    "endpoint_name": "athlete",
                    "endpoint_url": "v3/athlete",
                    "data_fetches": [
                        {
                            "date_downloaded": "22102019",
                        }
                    ]
                }
            ]
        }

    @classmethod
    def build_strava_data_provider_objects(cls):
        from dataproviders.models import DataProvider
        dp = DataProvider.create(
            MockDataProvider.build_strava_data_provider_json()
        )
        return dp

    @classmethod
    def create_data_provider_with_endpoints(cls):
        from dataproviders.models import DataProvider
        data_provider = DataProvider.objects.create(
            provider_name="dsfsd4",
            api_type=ApiTypes.OAUTH_GRAPHQL.value
        )
        data_provider.save()
        from dataproviders.models import Endpoint
        endpoint = Endpoint.objects.create(
            data_provider=data_provider,
            endpoint_name="test1",
            endpoint_url="testurl"
        )
        endpoint.save()
        endpoint2 = Endpoint.objects.create(
            data_provider=data_provider,
            endpoint_name="test2",
            endpoint_url="testurl"
        )
        endpoint2.save()
        return data_provider

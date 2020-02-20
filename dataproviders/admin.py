from django.contrib import admin

from MetaDataApi.utils.django_utils.base_model_admin import BaseModelAdmin
from dataproviders import tasks
from dataproviders.models import DataProvider, Endpoint, DataFetch, OauthConfig, HttpConfig, \
    DataProviderUser, DataFileUpload
from dataproviders.models.DataFile import DataFile
from dataproviders.services import oauth, InitializeDataProviders

models = (
    OauthConfig,
    HttpConfig,
)

[admin.site.register(model) for model in models]


@admin.register(Endpoint)
class EndpointAdmin(BaseModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['endpoint_name']
    model = Endpoint

    def fetch_data_from_endpoint(self, request, queryset):
        for endpoint in queryset:
            tasks.fetch_data_from_endpoint.delay(endpoint.data_provider.provider_name, endpoint.endpoint_name,
                                                 request.user.pk)

    actions = ["fetch_data_from_endpoint"]


class DataProviderAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['provider_name']

    def save_to_json_file(self, request, queryset):
        for data_provider in queryset:
            InitializeDataProviders.update_data_provider_to_json_file(data_provider)

    def reload_data_providers(self, request, queryset):
        InitializeDataProviders.load()

    actions = ["save_to_json_file", "reload_data_providers"]


admin.site.register(DataProvider, DataProviderAdmin)


@admin.register(DataFetch)
class DataFetchAdmin(BaseModelAdmin):
    model = DataFetch


@admin.register(DataFile)
class DataFileAdmin(BaseModelAdmin):
    model = DataFile


@admin.register(DataFileUpload)
class DataFileUploadAdmin(BaseModelAdmin):
    model = DataFileUpload


@admin.register(DataProviderUser)
class DataProviderUserAdmin(admin.ModelAdmin):
    # list_display = ['profile__user__username', 'provider__provider_name']
    # ordering = ['profile']
    actions = [
        "refresh_token",
    ]

    def refresh_token(self, request, queryset):
        for data_provider_user in queryset:
            oauth.refresh_access_token(data_provider_user)

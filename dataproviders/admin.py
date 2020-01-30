from django.contrib import admin

# Register your models here.
from MetaDataApi.utils.django_model_utils.base_model_admin import BaseModelAdmin
from dataproviders import tasks
from dataproviders.models import DataProvider, Endpoint, DataDump, OauthConfig, HttpConfig, \
    DataProviderUser
from dataproviders.services import oauth

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

    def fetch_datadump_from_endpoint(self, request, queryset):
        for endpoint in queryset:
            tasks.fetch_data_from_endpoint.delay(endpoint.data_provider.provider_name, endpoint.endpoint_name,
                                                 request.user.pk)

    actions = ["fetch_datadump_from_endpoint"]


class DataProviderAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['provider_name']


admin.site.register(DataProvider, DataProviderAdmin)


@admin.register(DataDump)
class DataDumpAdmin(BaseModelAdmin):
    model = DataDump


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

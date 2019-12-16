from django.contrib import admin

# Register your models here.
from dataproviders.models import DataProvider, Endpoint, DataDump, OauthConfig, HttpConfig, \
    DataProviderUser


class EndpointAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['endpoint_name']
    actions = [
    ]


class DataProviderAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['provider_name']
    actions = [
    ]


admin.site.register(DataProvider, DataProviderAdmin)
admin.site.register(Endpoint, EndpointAdmin)

models = (
    DataDump,
    OauthConfig,
    HttpConfig,
)

[admin.site.register(model) for model in models]


class DataProviderUserAdmin(admin.ModelAdmin):
    # list_display = ['profile__user__username', 'provider__provider_name']
    # ordering = ['profile']
    actions = [
        # identify_schema_and_data_from_all_endpoints,
    ]


admin.site.register(DataProviderUser, DataProviderUserAdmin)

from django.contrib import admin

# Register your models here.
from dataproviders.models import DataProvider, Endpoint, DataDump, OauthConfig, HttpConfig, \
    DataProviderUser
from dataproviders.services import oauth


class EndpointAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['endpoint_name']
    actions = [
    ]


class DataProviderAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['provider_name']
    actions = []


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
        "refresh_token",
    ]

    def refresh_token(self, request, queryset):
        for data_provider_user in queryset:
            oauth.refresh_access_token(data_provider_user)


admin.site.register(DataProviderUser, DataProviderUserAdmin)

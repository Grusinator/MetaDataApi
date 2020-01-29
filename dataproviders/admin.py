from django.contrib import admin

# Register your models here.
from dataproviders.models import DataProvider, Endpoint, DataDump, OauthConfig, HttpConfig, \
    DataProviderUser
from dataproviders.services import oauth

models = (
    OauthConfig,
    HttpConfig,
)

[admin.site.register(model) for model in models]

def add_methods_to_admin_class(admin_class, methods):
    for method in methods:
        admin_class.actions.append(method.__name__)
        setattr(admin_class, method)


class EndpointAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['endpoint_name']
    actions = []
admin.site.register(Endpoint, EndpointAdmin)

class DataProviderAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['provider_name']
    actions = []

admin.site.register(DataProvider, DataProviderAdmin)


add_actions_to_datadump_admin = []

class DataDumpAdmin(admin.ModelAdmin):
    # list_display = ['profile__user__username', 'provider__provider_name']
    # ordering = ['profile']
    actions = []

add_actions_to_datadump_admin(DataDumpAdmin, add_actions_to_datadump_admin)

admin.site.register(DataDump, DataDumpAdmin)


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

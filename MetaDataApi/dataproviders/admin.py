from django.contrib import admin

# Register your models here.
from dataproviders.models import ThirdPartyDataProvider
from dataproviders.services import AddDefaultDataProviderService


def add_default_providers(modeladmin, request, queryset):

    AddDefaultDataProviderService.execute({
        "provider_name": "all",  # means all
    })


add_default_providers.short_description = "add all default dataproviders"


class ThirdPartyDataProviderAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['provider_name']
    actions = [
        add_default_providers
    ]


admin.site.register(ThirdPartyDataProvider, ThirdPartyDataProviderAdmin)

from django.contrib import admin

# Register your models here.
from MetaDataApi.dataproviders.models import DataProvider


class ThirdPartyDataProviderAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['provider_name']
    actions = [
    ]


admin.site.register(DataProvider, ThirdPartyDataProviderAdmin)

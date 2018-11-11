from django.contrib import admin

# Register your models here.
from MetaDataApi.users.models import Profile, ThirdPartyProfile

from MetaDataApi.metadata.services import *
admin.site.register(Profile)


def identify_schema_from_all_endpoints(modeladmin, request, queryset):

    for thd_part_profile in queryset:
        n_objs = IdentifySchemaFromProviderService.execute({
            "provider_name": thd_part_profile.provider.provider_name,
            "endpoint": "all",
            "user_pk": thd_part_profile.profile.user.pk,
        })


identify_schema_from_all_endpoints.short_description = "identify_schema_from_all_endpoints"


def identify_data_from_all_endpoints(modeladmin, request, queryset):

    for thd_part_profile in queryset:
        n_objs = IdentifyDataFromProviderService.execute({
            "provider_name": thd_part_profile.provider.provider_name,
            "endpoint": "all",
            "user_pk": thd_part_profile.profile.user.pk,
        })


identify_data_from_all_endpoints.short_description = "identify_data_from_all_endpoints"


class ThirdPartyProfileAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    # ordering = ['profile']
    actions = [
        identify_schema_from_all_endpoints,
        identify_data_from_all_endpoints
    ]


admin.site.register(ThirdPartyProfile, ThirdPartyProfileAdmin)

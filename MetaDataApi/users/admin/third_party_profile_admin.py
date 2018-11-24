from django.contrib import admin

# Register your models here.
from MetaDataApi.users.models import Profile, ThirdPartyProfile
from MetaDataApi.metadata.services import IdentifySchemaAndDataFromProviderService


def identify_schema_and_data_from_all_endpoints(modeladmin, request, queryset):

    for thd_part_profile in queryset:
        n_objs = IdentifySchemaAndDataFromProviderService.execute({
            "provider_name": thd_part_profile.provider.provider_name,
            "endpoint": "all",
            "user_pk": thd_part_profile.profile.user.pk,
        })


identify_schema_and_data_from_all_endpoints.short_description = "identify_schema_and_data_from_all_endpoints"


class ThirdPartyProfileAdmin(admin.ModelAdmin):
    # list_display = ['profile__user__username', 'provider__provider_name']
    # ordering = ['profile']
    actions = [
        identify_schema_and_data_from_all_endpoints,
    ]


admin.site.register(ThirdPartyProfile, ThirdPartyProfileAdmin)

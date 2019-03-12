import json

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import (
    ObjectDoesNotExist)
from service_objects.services import Service

from dataproviders.default_3rd_data_providers import default_data_providers
from dataproviders.models import third_party_data_provider
from dataproviders.services.data_provider_etl_service import DataProviderEtlService


class AddDefaultDataProviderService(Service):
    provider_name = forms.CharField()

    def process(self):
        provider_name = self.cleaned_data['provider_name']

        default_providers = default_data_providers

        # select only the chosen one if not
        if provider_name != "all":
            provider = list(filter(lambda x: x.provider_name == provider_name,
                                   default_data_providers))
            if provider:
                default_providers = [provider, ]

        for dp in default_providers:
            # test if it exists before creating it
            try:
                third_party_data_provider.objects.get(
                    provider_name=dp.provider_name)
            except ObjectDoesNotExist:
                dp.save()

        return default_data_providers


class LoadDataFromProviderService(Service):
    """Read the raw data from endpoint"""

    provider_name = forms.CharField()
    user_pk = forms.IntegerField()
    endpoint = forms.CharField(required=False)

    def process(self):
        provider_name = self.cleaned_data['provider_name']
        endpoint = self.cleaned_data['endpoint']
        user_pk = self.cleaned_data['user_pk']
        user = User.objects.get(pk=user_pk)

        # get the dataprovider
        data_provider = third_party_data_provider.objects.get(
            provider_name=provider_name)
        # init service
        service = DataProviderEtlService(data_provider)
        # get the profile, with the access token matching the provider_name
        thirdpartyprofiles = user.profile.data_provider_profiles
        thirdpartyprofile = thirdpartyprofiles.get(
            provider__provider_name=provider_name)

        # request
        if endpoint == "all":
            endpoints = json.loads(data_provider.rest_endpoints_list)
        else:
            endpoints = [endpoint, ]

        data = [service.read_data_from_endpoint(
            ep, thirdpartyprofile.access_token) for ep in endpoints]

        return data

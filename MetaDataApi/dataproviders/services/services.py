import json

from django import forms
from django.contrib.auth.models import User
from service_objects.services import Service

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.dataproviders.services.data_provider_etl_service import DataProviderEtlService


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
        data_provider = DataProvider.objects.get(
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

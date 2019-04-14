from datetime import datetime

from django import forms
from service_objects.services import Service

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.metadata.rdf_models.rdf_data_provider import RdfDataProvider


class CreateRdfDataProviderEndpointService(Service):
    provider_name = forms.CharField()
    url = forms.FileField()
    endpoint_name = forms.CharField()

    def process(self):
        provider_name = self.cleaned_data['provider_name']
        url = self.changed_data['url']
        endpoint_name = self.changed_data['endpoint_name']

        provider = DataProvider.exists(provider_name)
        RdfDataProvider.create_endpoint_to_data_provider(
            provider.data_provider_instance,
            endpoint_url=url,
            endpoint_name=endpoint_name
        )


class CreateRdfDataProviderService(Service):
    provider_name = forms.CharField()
    rest_endpoint_name = forms.CharField()
    file = forms.FileField()

    def process(self):
        provider_name = self.cleaned_data['provider_name']
        rest_endpoint_name = self.cleaned_data['rest_endpoint_name']
        file = self.changed_data['file']
        provider = DataProvider.exists(provider_name)
        rest_endpoint = RdfDataProvider.get_endpoint(provider.data_provider_instance, rest_endpoint_name)
        RdfDataProvider.create_data_dump(rest_endpoint, datetime.now(), file)

import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider import Endpoint

logger = logging.getLogger(__name__)


class DataProviderView:
    @staticmethod
    def data_provider_list(request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        data_providers = DataProvider.objects.all()

        return render(request, 'dataproviders.html',
                      {
                          "dataproviders": data_providers,
                          "user_id": request.user.pk
                      })

    @staticmethod
    def data_provider(request, provider_name):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        dataprovider = DataProviderView.get_data_provider(provider_name)
        endpoints = Endpoint.get_all_endpoints_as_objects(dataprovider.data_provider_instance)

        return render(
            request,
            'dataprovider_detail.html',
            {
                "dataprovider": dataprovider,
                "endpoints": endpoints,
                "user_id": request.user.pk
            }
        )

    @staticmethod
    def get_data_provider(provider_name):
        try:
            dataprovider = DataProvider.objects.get(provider_name=provider_name)
        except ObjectDoesNotExist:
            raise Http404('provider does not exist')
        return dataprovider



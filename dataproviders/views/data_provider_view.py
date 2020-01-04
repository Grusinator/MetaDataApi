import logging

from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render

from dataproviders.models import DataProvider
from dataproviders.services.initialize_data_providers import InitializeDataProviders

logger = logging.getLogger(__name__)


class DataProviderView:
    @staticmethod
    def data_provider_list(request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        if request.method == "POST":
            InitializeDataProviders.load()
            return redirect('providers')
        else:
            data_providers = DataProvider.objects.all()

            return render(request, 'dataproviders.html',
                          {
                              "dataproviders": data_providers,
                              "user_id": request.user.pk,
                          })

    @staticmethod
    def data_provider(request, provider_name):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        data_provider = DataProvider.objects.get(provider_name=provider_name)
        endpoints = data_provider.endpoints.all()
        oauth_config = data_provider.oauth_config

        return render(request, 'dataprovider_detail.html',
                      {
                          "data_provider": data_provider,
                          "authorize_url": oauth_config.build_auth_url(request.user.pk),
                          "endpoints": endpoints,
                          "user_id": request.user.pk
                      }
                      )

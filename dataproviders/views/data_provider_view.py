import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from dataproviders.models import DataProvider, DataProviderUser
from dataproviders.services.initialize_data_providers import InitializeDataProviders

logger = logging.getLogger(__name__)


@login_required
def data_provider_list_view(request):
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


@login_required
def data_provider_view(request, provider_name):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    data_provider = DataProvider.objects.get(provider_name=provider_name)
    endpoints = data_provider.endpoints.all()
    oauth_auth_url = try_get_oauth_url(data_provider, request)
    data_provider_user = DataProviderUser.objects.filter(data_provider=data_provider, user=request.user).first()

    return render(request, 'dataprovider_detail.html',
                  {
                      "data_provider": data_provider,
                      "oauth_authorize_url": oauth_auth_url,
                      "endpoints": endpoints,
                      "user_id": request.user.pk,
                      "data_provider_user": data_provider_user
                  }
                  )


def try_get_oauth_url(data_provider, request):
    try:
        return data_provider.oauth_config.build_auth_url(request.user.pk)
    except:
        return None

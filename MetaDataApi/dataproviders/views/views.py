import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.metadata.rdf_models import RdfDataProvider

logger = logging.getLogger(__name__)


# Create your views here.


def data_provider_list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    data_providers = DataProvider.objects.all()

    return render(request, 'dataproviders.html',
                  {
                      "dataproviders": data_providers,
                      "user_id": request.user.pk
                  })


def data_provider(request, provider_name):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    try:
        dataprovider = DataProvider.objects.get(provider_name=provider_name)
    except ObjectDoesNotExist:
        raise Http404('provider does not exist')

    endpoints = RdfDataProvider.get_all_endpoints_as_objects(dataprovider.data_provider_instance)

    rendering = render(
        request,
        'dataprovider_detail.html',
        {
            "dataprovider": dataprovider,
            "endpoints": endpoints,
            "user_id": request.user.pk
        }
    )
    return rendering

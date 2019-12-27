import logging

from django.http import Http404
from django.shortcuts import render

from dataproviders.models import DataProvider
from dataproviders.services.fetch_data_from_provider import fetch_data_from_endpoint

logger = logging.getLogger(__name__)


def endpoint_detail_view(request, provider_name, endpoint_name):
    data_provider = DataProvider.objects.get(provider_name=provider_name)
    endpoint = data_provider.endpoints.get(endpoint_name=endpoint_name)

    handle_store_data(endpoint_name, provider_name, request)

    data_dumps = list(endpoint.data_dumps.all())
    data_dumps.sort(key=lambda x: x.date_downloaded, reverse=True)

    return render(
        request,
        'endpoint_detail.html',
        {
            "data_provider": data_provider,
            "endpoint": endpoint,
            "data_dumps": data_dumps,
            "user_id": request.user.pk
        }
    )


def handle_store_data(endpoint_name, provider_name, request):
    if request.GET.get('store_data', False):
        try:
            fetch_data_from_endpoint(provider_name, endpoint_name, request.user.pk)
        except Exception as e:
            error_msg = 'data error: %s' % e
            logger.error(error_msg)
            raise Http404(error_msg)

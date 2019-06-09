import logging

from django.http import Http404
from django.shortcuts import render

from MetaDataApi.dataproviders.models import Endpoint
from MetaDataApi.dataproviders.services.services import StoreDataFromProviderService
from MetaDataApi.dataproviders.views import DataProviderView
from MetaDataApi.metadata.services.services import LoadSchemaAndDataFromDataDump

logger = logging.getLogger(__name__)


def endpoint_detail_view(request, provider_name, endpoint_name):
    dataprovider = DataProviderView.get_data_provider(provider_name)
    endpoint = Endpoint.get_endpoint_as_object(
        dataprovider.data_provider_instance,
        endpoint_name
    )

    handle_load_data_from_dump(request)
    handle_store_data(endpoint_name, provider_name, request)

    data_dumps = endpoint.data_dumps
    data_dumps.sort(key=lambda x: x.date_downloaded, reverse=True)

    return render(
        request,
        'endpoint_detail.html',
        {
            "dataprovider": dataprovider,
            "endpoint": endpoint,
            "data_dumps": data_dumps,
            "user_id": request.user.pk
        }
    )


def handle_load_data_from_dump(request):
    load_data_dump_pk = request.GET.get('load_file', None)
    if load_data_dump_pk:
        try:
            LoadSchemaAndDataFromDataDump.execute({
                "data_dump_pk": int(load_data_dump_pk),
                "user_pk": request.user.pk
            })
        except NotImplementedError as e:
            error_msg = 'data error: %s' % e
            logger.error(error_msg)
            raise Http404(error_msg)


def handle_store_data(endpoint_name, provider_name, request):
    if request.GET.get('store_data', False):
        try:
            StoreDataFromProviderService.execute({
                "provider_name": provider_name,
                "endpoint_name": endpoint_name,
                "user_pk": request.user.pk
            })
        except Exception as e:
            error_msg = 'data error: %s' % e
            logger.error(error_msg)
            raise Http404(error_msg)

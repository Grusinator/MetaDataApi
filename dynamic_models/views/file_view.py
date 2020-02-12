import logging

from django.http import Http404
from django.shortcuts import render

from dataproviders.models import DataFetch

logger = logging.getLogger(__name__)
from dynamic_models import services


def files_view(request):
    handle_build_model(request)
    handle_load_data(request)
    data_fetches = DataFetch.objects.filter(user=request.user)
    return render(request, 'file_list_view.html', {"data_fetches": data_fetches})


def handle_build_model(request):
    dump_pk = request.POST.get('build_model', False)
    if dump_pk:
        data_fetch = DataFetch.objects.get(pk=dump_pk)
        try:
            services._try_build_model_from_data_file(data_fetch)
        except Exception as e:
            error_msg = 'data error: %s' % e
            logger.error(error_msg)
            raise Http404(error_msg)


def handle_load_data(request):
    dump_pk = request.POST.get('load_data', False)
    if dump_pk:
        data_fetch = DataFetch.objects.get(pk=dump_pk)
        try:
            services._try_load_data_from_data_file(data_fetch)
        except Exception as e:
            error_msg = 'data error: %s' % e
            logger.error(error_msg)
            raise Http404(error_msg)

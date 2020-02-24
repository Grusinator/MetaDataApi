from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from MetaDataApi.utils.django_utils import django_file_utils
from dataproviders.models import DataFetch


@login_required
def data_fetch_view(request, file_name):
    data_fetch = DataFetch.objects.get(data_file_from_source=settings.DATAFILE_STORAGE_PATH + file_name)
    file_content = django_file_utils.convert_file_to_str(data_fetch.data_file_from_source)
    return render(request, 'data_file.html', {"file_content": file_content})

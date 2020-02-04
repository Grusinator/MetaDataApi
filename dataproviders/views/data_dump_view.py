from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from MetaDataApi.utils.django_model_utils import DjangoModelUtils
from dataproviders.models import DataFetch


@login_required
def data_dump_view(request, file_name):
    data_dump = DataFetch.objects.get(file=settings.DATAFILE_STORAGE_PATH + file_name)
    file_content = DjangoModelUtils.convert_file_to_str(data_dump.file)
    return render(request, 'data_file.html', {"file_content": file_content})

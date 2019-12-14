from django.shortcuts import render

from MetaDataApi.utils.django_model_utils import DjangoModelUtils
from dataproviders.models import DataDump


def data_dump_view(request, file_name):
    data_dump = DataDump.objects.get(file=DataDump.storage_path + file_name)
    file_content = DjangoModelUtils.convert_file_to_str(data_dump.file)
    return render(
        request,
        'data_file.html',
        {
            "file_content": file_content
        }
    )
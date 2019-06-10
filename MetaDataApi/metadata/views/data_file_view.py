from django.shortcuts import render

from MetaDataApi.dataproviders.models import DataDump
from MetaDataApi.metadata.models import FileAttribute
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils


def data_file_view(request, file_name):
    storage_path = FileAttribute.storage_path
    file_instance = FileAttribute.objects.get(value=storage_path + file_name)
    file_content = DjangoModelUtils.convert_file_to_str(file_instance.value)
    return render(
        request,
        'data_file.html',
        {
            "file_content": file_content
        }
    )


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

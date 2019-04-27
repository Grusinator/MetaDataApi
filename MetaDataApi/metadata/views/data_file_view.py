from django.shortcuts import render

from MetaDataApi.metadata.models import FileAttributeInstance
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils


def data_file_view(request, file_name):
    storage_path = FileAttributeInstance.storage_path
    file_instance = FileAttributeInstance.objects.get(value=storage_path + file_name)
    file_content = DjangoModelUtils.convert_file_to_str(file_instance.value)
    return render(
        request,
        'data_file.html',
        {
            "file_content": file_content
        }
    )
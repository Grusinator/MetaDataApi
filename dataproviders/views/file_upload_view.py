from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from MetaDataApi.utils.django_utils.django_file_utils import get_default_file_name
from dataproviders.forms.file_upload_form import FileUploadForm
from dataproviders.models import DataProvider


@login_required
def file_upload_view(request, provider_name):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_upload = form.save(commit=False)
            file_upload.data_provider = DataProvider.objects.get(provider_name=provider_name)
            file_upload.user = request.user
            file_upload.data_file_from_source.name = get_default_file_name(
                based_on=file_upload.data_file_from_source.name)
            file_upload.save()
            return redirect(f"providers/{provider_name}")
    else:
        form = FileUploadForm()
    return render(request, 'file_upload.html', {
        'form': form,
        'provider_name': provider_name
    })

from django.shortcuts import render

from MetaDataApi.dynamic_models.services import load_data_from_provider_dumps


def dynamic_models_view(request):
    if request.method == "POST":
        load_data_from_provider_dumps()
    else:
        pass
    return render(request, 'dynamic_models.html')

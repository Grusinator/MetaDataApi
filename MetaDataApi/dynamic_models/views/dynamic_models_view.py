from django.shortcuts import render

from MetaDataApi.dynamic_models.tasks import load_data_from_provider_dumps


def dynamic_models_view(request):
    if request.method == "POST":
        load_data_from_provider_dumps.delay()
    else:
        pass
    return render(request, 'dynamic_models.html')

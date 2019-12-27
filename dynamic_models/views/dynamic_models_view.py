from django.shortcuts import render

from dynamic_models.tasks import build_models_from_provider_dumps


def dynamic_models_view(request):
    if request.method == "POST":
        build_models_from_provider_dumps.delay()
    else:
        pass
    return render(request, 'dynamic_models.html')

from django.shortcuts import render
from MetaDataApi.dataproviders.models import ThirdPartyDataProvider

# Create your views here.


def data_provider_list(request):
    data_providers = ThirdPartyDataProvider.objects.all()
    return render(request, 'dataproviders.html',
                  {"dataproviders": data_providers})

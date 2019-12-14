from django.conf.urls import url
from django.urls import path

from dataproviders.views import DataProviderView, oauth2redirect_view
from dataproviders.views.endpoint_detail_view import endpoint_detail_view

urlpatterns = [
    path('', DataProviderView.data_provider_list, name='providers'),
    path('<str:provider_name>', DataProviderView.data_provider, name='provider_detail'),
    path('<str:provider_name>/endpoint/<str:endpoint_name>', endpoint_detail_view, name='endpoint_detail'),
    url(r'^oauth2redirect/$', oauth2redirect_view, name='oauth2redirect'),
]

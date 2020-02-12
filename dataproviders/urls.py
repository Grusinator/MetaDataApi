from django.conf.urls import url
from django.urls import path

from dataproviders.views import oauth2redirect_view, file_upload_view
from dataproviders.views.data_fetch_view import data_fetch_view
from dataproviders.views.data_provider_view import data_provider_list_view, data_provider_view
from dataproviders.views.endpoint_detail_view import endpoint_detail_view

urlpatterns = [
    path('', data_provider_list_view, name='providers'),
    path('<str:provider_name>/', data_provider_view, name='provider_detail'),
    path('<str:provider_name>/endpoint/<str:endpoint_name>/', endpoint_detail_view, name='endpoint_detail'),
    path('<str:provider_name>/upload_file/', file_upload_view, name="file_upload"),
    url(r'^oauth2redirect/$', oauth2redirect_view, name='oauth2redirect'),
    path('data_fetches/<str:file_name>', data_fetch_view, name='data_fetch_detail'),
]

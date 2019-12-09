from django.urls import path

from MetaDataApi.dataproviders.views import DataProviderView
from MetaDataApi.dataproviders.views.endpoint_detail_view import endpoint_detail_view
from MetaDataApi.metadata.views.data_file_view import data_file_view, data_dump_view

urlpatterns = [
    path('', DataProviderView.data_provider_list, name='providers'),
    path('<str:provider_name>', DataProviderView.data_provider, name='provider_detail'),
    path('<str:provider_name>/endpoint/<str:endpoint_name>', endpoint_detail_view, name='endpoint_detail'),
    path('datafiles/<str:file_name>', data_file_view, name='datafile'),
    path('data_dumps/<str:file_name>', data_dump_view, name='data_dump'),
]

from django.urls import path

from .views.dynamic_data_detail_view import dynamic_data_detail_view
from .views.dynamic_data_list_view import dynamic_data_list_view

urlpatterns = [
    path('', dynamic_data_list_view, name="dynamic_data_list"),
    path('<str:model_name>/<int:pk>/', dynamic_data_detail_view, name="dynamic_data_detail"),
]

from django.urls import path

from .views.dynamic_data_instances_view import dynamic_data_instances_view
from .views.object_views import model_list_view

urlpatterns = [
    path('', dynamic_data_instances_view, name="dynamic_data_instances"),
    path('objects/<str:object_label>', model_list_view, name="model_list"),
]

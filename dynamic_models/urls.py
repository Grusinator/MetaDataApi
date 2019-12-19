from django.urls import path

from .views.create import create_models_from_json_view
from .views.dynamic_models_view import dynamic_models_view
from .views.file_view import files_view
from .views.object_views import model_list_view

urlpatterns = [
    path('', dynamic_models_view),
    path('create/', create_models_from_json_view, name='create_models'),
    path('objects/<str:object_label>', model_list_view, name="model_list"),
    # path('/objects/<str:object_label>/<str:pk>', , name='object_detail'),
    path('files/', files_view, name="files")
]

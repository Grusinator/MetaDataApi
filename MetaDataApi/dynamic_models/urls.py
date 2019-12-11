from django.urls import path

from MetaDataApi.dynamic_models.views.create import create_models_from_json_view
from MetaDataApi.dynamic_models.views.dynamic_models_view import dynamic_models_view
from MetaDataApi.dynamic_models.views.object_views import model_list_view

urlpatterns = [
    path('', dynamic_models_view),
    path('create/', create_models_from_json_view, name='create_models'),
    path('objects/<str:object_label>', model_list_view, name="model_list"),
    # path('/objects/<str:object_label>/<str:pk>', , name='object_detail'),
]

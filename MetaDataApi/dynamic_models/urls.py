from django.urls import path

from MetaDataApi.dynamic_models.views.create import create_models_from_json_view
from MetaDataApi.dynamic_models.views.object_views import build_object_list_view

person_view = build_object_list_view(None, None, "person")
urlpatterns = [
    path('create/', create_models_from_json_view, name='create_models'),
    # path('<str:provider_name>/objects/<str:object_label>', person_view.as_view()),
    # path('<str:provider_name>/objects/<str:object_label>/<str:pk>', build_object_detail_view, name='object_detail'),
]

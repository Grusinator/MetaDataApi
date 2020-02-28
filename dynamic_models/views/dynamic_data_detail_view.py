from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model

from dynamic_models.views.dynamic_view_object import DynamicViewObject


@login_required
def dynamic_data_detail_view(request, model_name, pk):
    user_pk = request.user.pk
    model = get_dynamic_model(model_name)
    instance = model.objects.get(pk=pk, user_pk=user_pk)
    html_params = {"instance": DynamicViewObject(instance)}
    return render(request, 'dynamic_data_detail.html', html_params)

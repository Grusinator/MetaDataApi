from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model, get_all_model_definition_names

from dynamic_models.views.dynamic_view_object import DynamicViewObject


@login_required
def dynamic_data_instances_view(request):
    user_pk = request.user.pk
    model_names = get_all_model_definition_names()
    selected_model_name = request.GET.get('model')
    order_by = request.GET.get('order_by')
    html_params = {"model_names": model_names, "selected_model_name": selected_model_name}
    if selected_model_name:
        model = get_dynamic_model(selected_model_name)
        instances = model.objects.filter(user_pk=user_pk)[:100]
        view_instances = [DynamicViewObject(inst) for inst in instances]
        html_params["dynamic_data_instances"] = view_instances
        html_params["field_names"] = view_instances[0].field_names if model else None
    return render(request, 'dynamic_data_instances.html', html_params)

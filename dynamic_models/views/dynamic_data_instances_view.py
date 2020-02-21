from django.shortcuts import render
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model

from dynamic_models.views.dynamic_view_object import DynamicViewObject


def dynamic_data_instances_view(request):
    model_name = request.GET.get('model')
    order_by = request.GET.get('order_by')
    model = get_dynamic_model(model_name or "")

    instances = model.objects.filter()[:100]
    view_instances = [DynamicViewObject(inst) for inst in instances]
    field_names = view_instances[0].field_names if model else None
    return render(request, 'dynamic_data_instances.html',
                  {"dynamic_data_instances": view_instances,
                   "model_name": model_name,
                   "field_names": field_names})

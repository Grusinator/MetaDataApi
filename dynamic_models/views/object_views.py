from django.shortcuts import render
from django.views import generic
from json2model.services.dynamic_model import get_dynamic_model


def build_object_list_view(request, provider_name, object_label):
    # object_label = request.GET.get("object_label")
    model = get_dynamic_model(object_label)
    attrs = {"model": model}
    list_view = type(f"{model.__name__}ListView", (generic.ListView,), attrs)
    return list_view


def build_object_detail_view(request, provider_name, object_label):
    # object_label = request.GET.get("object_label")
    model = get_dynamic_model(object_label)
    attrs = {"model": model}
    return type(f"{model.__name__}DetailView", (generic.DetailView,), attrs)  # .as_view()


def model_list_view(request, object_label):
    model = get_dynamic_model(object_label)
    fields = model._meta.fields
    instances = model.objects.all()
    return render(request, 'object_list.html', {'object_label': object_label, 'instances': instances})

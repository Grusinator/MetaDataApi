import operator
from functools import reduce

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import TextField, Q
from django.shortcuts import render
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model, get_all_model_definition_names

from dynamic_models.schema import get_all_field_names_of_type
from dynamic_models.views.dynamic_view_object import DynamicViewObject


def bitwise_any(a_list):
    return reduce(operator.or_, a_list, Q())


def build_search_args(model, search_query):
    text_field_names = get_all_field_names_of_type(model, (TextField,))
    query_elm = [Q(**{f"{text_field_name}__icontains": search_query}) for text_field_name in text_field_names]
    query = bitwise_any(query_elm)
    return query


@login_required
def dynamic_data_instances_view(request):
    user_pk = request.user.pk
    model_names = get_all_model_definition_names()
    selected_model_name = request.GET.get('model')
    order_by = request.GET.get('order_by')
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', 1)
    html_params = {"model_names": model_names, "selected_model_name": selected_model_name, "search_query": search_query}
    if selected_model_name:
        model = get_dynamic_model(selected_model_name)
        instances = query_instances(model, search_query, user_pk)
        # TODO figure out a smart way to only create dynamicViewObjects of insances in page
        view_instances = [DynamicViewObject(inst) for inst in instances]
        view_instances = make_paginator(page, view_instances)
        html_params["view_instances"] = view_instances
        html_params["field_names"] = view_instances[0].field_names if model and len(instances) else None
    return render(request, 'dynamic_data_instances.html', html_params)


def query_instances(model, search_query, user_pk):
    search_args = build_search_args(model, search_query)
    return model.objects.filter(search_args, user_pk=user_pk)


def make_paginator(page, view_instances):
    paginator = Paginator(view_instances, 5)
    try:
        view_instances = paginator.page(page)
    except PageNotAnInteger:
        view_instances = paginator.page(1)
    except EmptyPage:
        view_instances = paginator.page(paginator.num_pages)
    return view_instances

import operator
from functools import reduce

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import TextField, Q
from django.shortcuts import render
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model, get_all_model_definition_names, \
    get_all_dynamic_models

from dynamic_models.schema import get_field_names
from dynamic_models.views.dynamic_view_object import DynamicViewObject


@login_required
def dynamic_data_list_view(request):
    user_pk = request.user.pk
    model_names = get_all_model_definition_names()
    selected_model_name = request.GET.get('model', "")
    order_by = request.GET.get('order_by')
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', "")
    html_params = {
        "model_names": model_names, "selected_model_name": selected_model_name, "search_query": search_query,
        "view_instances": create_view_instances(selected_model_name, search_query, user_pk, page)
    }
    return render(request, 'dynamic_data_list.html', html_params)


def create_view_instances(selected_model_name, search_query, user_pk, page):
    if selected_model_name == "":
        return []
    models = [get_dynamic_model(selected_model_name)] if selected_model_name != "ALL" else get_all_dynamic_models()
    view_instances = []
    for model in models:
        instances = query_instances(model, search_query, user_pk)
        # TODO figure out a smart way to only create dynamicViewObjects of instances in page
        view_instances.extend([DynamicViewObject(inst) for inst in instances])
    paged_view_instances = make_paginator(page, view_instances)
    return paged_view_instances


def query_instances(model, search_query, user_pk):
    search_args = build_search_args(model, search_query)
    return model.objects.filter(search_args, user_pk=user_pk)


def bitwise_any(a_list):
    return reduce(operator.or_, a_list, Q())


def build_search_args(model, search_query):
    if search_query:
        text_field_names = get_field_names(model, (TextField,))
        query_elm = [Q(**{f"{text_field_name}__icontains": search_query}) for text_field_name in text_field_names]
        query = bitwise_any(query_elm)
        return query
    else:
        return Q()


def make_paginator(page, view_instances):
    paginator = Paginator(view_instances, 50)
    try:
        view_instances = paginator.page(page)
    except PageNotAnInteger:
        view_instances = paginator.page(1)
    except EmptyPage:
        view_instances = paginator.page(paginator.num_pages)
    return view_instances

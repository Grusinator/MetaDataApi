from django.db.models import Model
from django.views.generic import ListView


def build_list_view_properties(model: Model):
    return {"model": model,
            "template_name": "default_dynamic_model_list_view_template"}


def build_dynamic_model_list_view(model: Model):
    list_properties = build_list_view_properties(model)
    return type(f"{model.__name__}ListView", (ListView,), list_properties)


def build_dynamic_model_detail_view(model: Model):
    pass

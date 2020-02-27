from typing import Union

import graphene
from django.db.models import Model, TextField, IntegerField, FloatField, BooleanField, DateTimeField
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from mutant.models import ModelDefinition

filter_attribute_types = (TextField, IntegerField, FloatField, BooleanField, DateTimeField)
attribute_types = filter_attribute_types


def build_dynamic_model_query():
    types = create_types_for_all_dynamic_models()
    query_properties = build_query_properties(types)
    return type('Query', (graphene.ObjectType,), query_properties)


def create_types_for_all_dynamic_models():
    model_defs = ModelDefinition.objects.all()
    graphene_types = [create_graphene_type(model_def.model_class()) for model_def in model_defs]
    return graphene_types


def create_graphene_type(model: Model):
    name = model.__name__
    meta_properties = {
        "model": model,
        "interfaces": (graphene.relay.Node,),
        # "fields": get_field_names(model),
        "filter_fields": build_filter_fields(model)
    }
    meta_class = type("Meta", (), meta_properties)
    properties = {"Meta": meta_class}
    return type(name, (DjangoObjectType,), properties)


def get_fields(model, types=attribute_types):
    return [field for field in model._meta.get_fields() if isinstance(field, types)]


def get_field_names(model, types=attribute_types):
    return [field.name for field in get_fields(model, types)]


def build_filter_fields(model, types=attribute_types) -> dict:
    return {field.name: get_data_type_filter_fields_key_value(field) for field in get_fields(model, types)}


def get_data_type_filter_fields_key_value(field: Union[filter_attribute_types]):
    data_type_mapper = {
        TextField: ['exact', 'in', 'icontains', 'istartswith'],
        FloatField: ['exact']
    }
    return data_type_mapper.get(type(field), data_type_mapper[FloatField])


def build_query_properties(graphene_types):
    properties = {}
    for graphene_type in graphene_types:
        properties.update(create_field_properties(graphene_type))
        properties.update(create_django_filter_connection_field_properties(graphene_type))
        properties.update(create_list_properties(graphene_type))
    return properties


def assert_model_has_user_ref(model):
    if not hasattr(model, "user_pk"):
        raise GraphQLError(
            "the object that you are trying to access is not tied to a user. try rebuilding the model")


def create_list_properties(graphene_type):
    model = graphene_type._meta.model
    name = f"all_{graphene_type.__name__}s"

    @login_required
    def resolver(self, info, **kwargs):
        user_pk = info.context.user.pk
        assert_model_has_user_ref(model)
        return model.objects.filter(user_pk=user_pk)

    properties = {
        name: graphene.List(graphene_type),
        f"resolve_{name}": resolver
    }
    return properties


def create_django_filter_connection_field_properties(graphene_type):
    model = graphene_type._meta.model
    name = f"filter_{graphene_type.__name__}s"

    @login_required
    def resolver(self, info, **kwargs):
        user_pk = info.context.user.pk
        assert_model_has_user_ref(model)
        return model.objects.filter(user_pk=user_pk, **kwargs)

    properties = {
        name: DjangoFilterConnectionField(graphene_type),
        f"resolve_{name}": resolver
    }
    return properties


def create_field_properties(graphene_type):
    model = graphene_type._meta.model
    name = graphene_type.__name__

    @login_required
    def resolver(self, info, **kwargs):
        user_pk = info.context.user.pk
        assert_model_has_user_ref(model)
        return model.objects.filter(user_pk=user_pk).first()

    properties = {
        name: graphene.relay.Node.Field(graphene_type),
        f"resolve_{name}": resolver
    }
    return properties

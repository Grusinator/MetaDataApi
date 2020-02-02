import graphene
from django.db.models import Model, TextField, IntegerField, FloatField, BooleanField
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from mutant.models import ModelDefinition

filter_attribute_types = (TextField, IntegerField, FloatField, BooleanField)
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
        "fields": get_all_field_names_of_type(model, attribute_types),
        "filter_fields": get_all_field_names_of_type(model, filter_attribute_types)
    }
    meta_class = type("Meta", (), meta_properties)
    properties = {"Meta": meta_class}
    return type(name, (DjangoObjectType,), properties)


def get_all_field_names_of_type(model, types) -> list:
    return [field.name for field in model._meta.get_fields() if isinstance(field, types)]


def build_query_properties(graphene_types):
    properties = {}
    for graphene_type in graphene_types:
        properties.update(create_field_properties(graphene_type))
        # properties.update(create_django_filter_connection_field_properties(graphene_type))
        properties.update(create_list_properties(graphene_type))
    return properties


def create_list_properties(graphene_type):
    model = graphene_type._meta.model
    name = f"all_{graphene_type.__name__}s"

    @login_required
    def resolver(self, info, **kwargs):
        user_pk = info.context.user.pk
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
        if not hasattr(model, "user_pk"):
            raise
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
        return model.objects.filter(user_pk=user_pk).first()

    properties = {
        name: graphene.relay.Node.Field(graphene_type),
        f"resolve_{name}": resolver
    }
    return properties

import graphene
from django.db.models import Model
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mutant.models import ModelDefinition


def create_query():
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
        "interfaces": (graphene.relay.Node,)
    }
    meta_class = type("Meta", (), meta_properties)
    properties = {"Meta": meta_class}
    return type(name, (DjangoObjectType,), properties)


def build_query_properties(graphene_types):
    properties = {}
    for graphene_type in graphene_types:
        properties[graphene_type.__name__] = graphene.relay.Node.Field(graphene_type)
        properties[f"all_{graphene_type.__name__}"] = DjangoFilterConnectionField(graphene_type)
    return properties

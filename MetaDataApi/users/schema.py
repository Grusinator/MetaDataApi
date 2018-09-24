from django.contrib.auth.models import User

import graphene
from graphene_django import DjangoObjectType

from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = User
        # interfaces = (Node, )
        # filter_fields = {
        #    'username': ['exact', 'icontains', 'istartswith'],
        #    'email': ['exact', 'icontains'],
        #   }


class Query(graphene.ObjectType):
    user = graphene.Field(UserType)

    @login_required
    def resolve_user(self, info):
        return info.context.user


class Mutation(graphene.ObjectType):
    pass

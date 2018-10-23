

from MetaDataApi.dataproviders.services.data_provider_etl_service import (
    DataProviderEtlService)

from MetaDataApi.dataproviders.default_3rd_data_providers import (
    default_data_providers)
import os
import shutil
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User
from MetaDataApi.settings import MEDIA_ROOT


from MetaDataApi.users.schema import UserType
from MetaDataApi.dataproviders.models import (
    ThirdPartyDataProvider)


class DataProviderNode(DjangoObjectType):
    class Meta:
        model = ThirdPartyDataProvider
        filter_fields = ['name', ]
        interfaces = (graphene.relay.Node, )


class AddDataProvider(graphene.Mutation):
    dataprovider = graphene.List(DataProviderNode)
    success = graphene.Boolean()

    class Arguments:
        url = graphene.String()

    def mutate(self, info, url):
        if url == "all":
            for dp in default_data_providers:
                dp.save()

        return AddDataProvider(
            success=True,
            dataprovider=default_data_providers)


class Query(graphene.ObjectType):
    data_provider = graphene.relay.Node.Field(DataProviderNode)
    all_data_providers = DjangoFilterConnectionField(DataProviderNode)

    def resolve_data_provider(self, info):
        return ThirdPartyDataProvider.objects.first()

    def resolve_all_data_providers(self, info):
        return ThirdPartyDataProvider.objects.all()


class Mutation(graphene.ObjectType):
    add_data_provider = AddDataProvider.Field()

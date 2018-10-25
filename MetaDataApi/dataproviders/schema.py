

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

from MetaDataApi.users.models import ThirdPartyProfile

from MetaDataApi.dataproviders.services.data_provider_etl_service \
    import DataProviderEtlService


class DataProviderNode(DjangoObjectType):
    class Meta:
        model = ThirdPartyDataProvider
        filter_fields = ['provider_name', ]
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


class LoadAllDataFromProvider(graphene.Mutation):
    data = graphene.List(graphene.String)

    class Arguments:
        name = graphene.String()

    @login_required
    def mutate(self, info, name):
        # get the dataprovider
        data_provider = ThirdPartyDataProvider.objects.get(provider_name=name)
        # init service
        service = DataProviderEtlService(data_provider)
        # get the profile, with the access token matching the name
        thirdpartyprofiles = info.context.user.profile.data_provider_profiles
        thirdpartyprofile = thirdpartyprofiles.get(provider__name=name)

        # request
        data = service.read_data_from_all_rest_endpoints(
            thirdpartyprofile.access_token)

        return LoadAllDataFromProvider(
            data=data)


class Query(graphene.ObjectType):
    data_provider = graphene.relay.Node.Field(DataProviderNode)
    all_data_providers = DjangoFilterConnectionField(DataProviderNode)

    def resolve_data_provider(self, info):
        return ThirdPartyDataProvider.objects.first()

    def resolve_all_data_providers(self, info):
        return ThirdPartyDataProvider.objects.all()


class Mutation(graphene.ObjectType):
    add_data_provider = AddDataProvider.Field()
    load_all_data_from_dataprovider = LoadAllDataFromProvider.Field()

import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.dataproviders.services import AddDefaultDataProviderService, LoadDataFromProviderService


class DataProviderNode(DjangoObjectType):
    class Meta:
        model = DataProvider
        filter_fields = ['provider_name', ]
        interfaces = (graphene.relay.Node, )


class AddDefaultDataProvider(graphene.Mutation):
    dataprovider = graphene.List(DataProviderNode)
    success = graphene.Boolean()

    class Arguments:
        provider_name = graphene.String()

    @login_required
    def mutate(self, info, provider_name):
        args = dict(locals())
        [args.pop(x) for x in ["info", "self"]]

        default_data_providers = AddDefaultDataProviderService.execute(args)

        return AddDefaultDataProvider(
            success=True,
            dataprovider=default_data_providers)


class LoadDataFromProvider(graphene.Mutation):
    data = graphene.List(graphene.String)

    class Arguments:
        provider_name = graphene.String()
        endpoint = graphene.String()

    @login_required
    def mutate(self, info, provider_name, endpoint="all"):
        args = dict(locals())
        [args.pop(x) for x in ["info", "self"]]
        args["user_pk"] = info.context.user.pk

        data = LoadDataFromProviderService.execute(args)

        return LoadDataFromProvider(
            data=data)


class Query(graphene.ObjectType):
    data_provider = graphene.relay.Node.Field(DataProviderNode)
    all_data_providers = DjangoFilterConnectionField(DataProviderNode)

    def resolve_data_provider(self, info):
        return DataProvider.objects.first()

    def resolve_all_data_providers(self, info):
        return DataProvider.objects.all()


class Mutation(graphene.ObjectType):
    add_data_provider = AddDefaultDataProvider.Field()
    load_data_from_dataprovider = LoadDataFromProvider.Field()

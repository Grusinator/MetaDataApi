import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from dataproviders.models import DataProvider, DataProviderUser
# from dataproviders.services import AddDefaultDataProviderService, LoadDataFromProviderService
from users.models import Profile


class DataProviderType(DjangoObjectType):
    class Meta:
        model = DataProvider
        filter_fields = ['provider_name', ]
        interfaces = (graphene.relay.Node,)


class DataProviderUserType(DjangoObjectType):
    class Meta:
        model = DataProviderUser


# class AddDefaultDataProvider(graphene.Mutation):
#     dataprovider = graphene.List(DataProviderType)
#     success = graphene.Boolean()
#
#     class Arguments:
#         provider_name = graphene.String()
#
#     @login_required
#     def mutate(self, info, provider_name):
#         args = dict(locals())
#         [args.pop(x) for x in ["info", "self"]]
#
#         default_data_providers = AddDefaultDataProviderService.execute(args)
#
#         return AddDefaultDataProvider(
#             success=True,
#             dataprovider=default_data_providers)


# class LoadDataFromProvider(graphene.Mutation):
#     data = graphene.List(graphene.String)
#
#     class Arguments:
#         provider_name = graphene.String()
#         endpoint = graphene.String()
#
#     @login_required
#     def mutate(self, info, provider_name, endpoint="all"):
#         args = dict(locals())
#         [args.pop(x) for x in ["info", "self"]]
#         args["user_pk"] = info.context.user.pk
#
#         data = LoadDataFromProviderService.execute(args)
#
#         return LoadDataFromProvider(
#             data=data)


class CreateThirdPartyProfile(graphene.Mutation):
    third_party_profile = graphene.Field(DataProviderUserType)

    class Arguments:
        provider = graphene.String()
        access_token = graphene.String()

    @login_required
    def mutate(self, info, provider, access_token, profile_json_field):
        third_party_profile = DataProviderUser(
            user=info.context.user,
            data_provider=provider,
            access_token=access_token
        )

        third_party_profile.save()

        return CreateThirdPartyProfile(third_party_profile=third_party_profile)


class Query(graphene.ObjectType):
    data_provider = graphene.relay.Node.Field(DataProviderType)
    all_data_providers = DjangoFilterConnectionField(DataProviderType)
    create_third_party_profile = CreateThirdPartyProfile.Field()
    third_party_profiles = graphene.List(DataProviderUserType)

    def resolve_data_provider(self, info):
        return DataProvider.objects.first()

    def resolve_all_data_providers(self, info):
        return DataProvider.objects.all()

    @login_required
    def resolve_third_party_profiles(self, info):
        profile = Profile.objects.get(user=info.context.user)
        return DataProviderUser.objects.filter(profile=profile)


class Mutation(graphene.ObjectType):
    pass
    # add_data_provider = AddDefaultDataProvider.Field()
    # load_data_from_dataprovider = LoadDataFromProvider.Field()

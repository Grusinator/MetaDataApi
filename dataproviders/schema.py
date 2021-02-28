import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from dataproviders.models import DataProvider, DataProviderUser
from users.models import Profile


class DataProviderType(DjangoObjectType):
    class Meta:
        model = DataProvider
        filter_fields = ['provider_name', ]
        interfaces = (graphene.relay.Node,)


class DataProviderUserType(DjangoObjectType):
    class Meta:
        model = DataProviderUser


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

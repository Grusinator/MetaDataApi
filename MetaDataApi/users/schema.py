from django.contrib.auth.models import User
from graphene import Mutation, String, ObjectType, Field, List, Date, Enum, Float
from graphene_django import DjangoObjectType
from graphql.error import GraphQLError
from graphql_jwt.decorators import login_required

from MetaDataApi.users.models import Profile, ThirdPartyProfile, Languages

GrapheneLanguages = Enum.from_enum(Languages)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        #interfaces = (Node, )
        # filter_fields = {
        #    'username': ['exact', 'icontains', 'istartswith'],
        #    'email': ['exact', 'icontains'],
        #   }


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        # Allow for some more advanced filtering here
        #interfaces = (graphene.Node, )
        # filter_fields = {
        #    'name': ['exact', 'icontains', 'istartswith'],
        #    'notes': ['exact', 'icontains'],
        # }


class ThirdPartyProfileType(DjangoObjectType):
    class Meta:
        model = ThirdPartyProfile


class CreateUser(Mutation):
    user = Field(UserType)

    class Arguments:
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)
        birthdate = Date()
        language = GrapheneLanguages()

    def mutate(self, info, username, password, email, birthdate=None, language="English"):
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        profile = Profile(
            birthdate=birthdate,
            user=user,
            language=language
        )
        profile.save()

        return CreateUser(user=user)


class UpdateProfile(Mutation):
    profile = Field(ProfileType)

    class Arguments:
        birthdate = Date()
        language = GrapheneLanguages()
        #profilepicture = Upload()
        audio_threshold = Float()

    @login_required
    def mutate(self, info, language, audio_threshold, birthdate=None):
        try:
            profile = Profile.objects.get(user=info.context.user)
        except Exception as e:
            raise GraphQLError(
                "profile object has not been created successfully: " + str(e))

        # update each attribute
        if birthdate is not None:
            profile.birthdate = birthdate
        if language is not None:
            profile.language = language
        if audio_threshold is not None:
            profile.audio_threshold = audio_threshold

        profile.save()

        return UpdateProfile(profile)


class CreateThirdPartyProfile(Mutation):
    third_party_profile = Field(ThirdPartyProfileType)

    class Arguments:
        provider = String()
        access_token = String()
        profile_json_field = String()

    @login_required
    def mutate(self, info, provider, access_token, profile_json_field):
        try:
            profile = Profile.objects.get(user=info.context.user)
        except Exception as e:
            raise GraphQLError(
                "profile object has not been created successfully: " + str(e))

        third_party_profile = ThirdPartyProfile(
            profile=profile,
            provider=provider,
            access_token=access_token,
            profile_json_field=profile_json_field)

        third_party_profile.save()

        return CreateThirdPartyProfile(third_party_profile=third_party_profile)


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_profile = UpdateProfile.Field()
    create_third_party_profile = CreateThirdPartyProfile.Field()


class Query(ObjectType):
    user = Field(UserType)
    profile = Field(ProfileType)
    third_party_profiles = List(ThirdPartyProfileType)

    @login_required
    def resolve_user(self, info):
        return info.context.user

    @login_required
    def resolve_profile(self, info):
        return Profile.objects.get(user=info.context.user)

    @login_required
    def resolve_third_party_profiles(self, info):
        profile = Profile.objects.get(user=info.context.user)
        return ThirdPartyProfile.objects.filter(profile=profile)

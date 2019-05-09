import logging

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import DataProviderO
from MetaDataApi.metadata.utils import JsonUtils
from MetaDataApi.settings import OAUTH_REDIRECT_URI
from MetaDataApi.users.models import DataProviderProfile
from MetaDataApi.users.models import Profile

logger = logging.getLogger(__name__)


class OauthRedirectRequestException(Exception):
    pass


def oauth2redirect_view(request):
    code = get_auth_code(request)
    scope = get_scope(request)
    profile = validate_and_get_profile(request)
    data_provider = validate_and_get_provider(request)

    access_token = request_acess_token(code, data_provider)

    save_data_provider_profile(access_token, data_provider, profile)
    return HttpResponse(
        """successfully connected your profile with %s
        <a href= "%s"> back <a> """
        % (data_provider.provider_name,
           "../providers/")
    )


def request_acess_token(code, data_provider):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": data_provider.client_id,
        "client_secret": data_provider.client_secret,
        "redirect_uri": OAUTH_REDIRECT_URI,
    }
    url = data_provider.access_token_url
    r = requests.post(url, data=data, allow_redirects=True)
    if not r.ok:
        raise OauthRedirectRequestException("the token request did not return with ok. Reason: %s" % r.reason)

    json_obj = JsonUtils.validate(r.content)

    access_token = json_obj.pop("access_token")
    token_type = json_obj.pop("token_type")

    if access_token is "" or None:
        raise OauthRedirectRequestException("access token was not found in response: %s" % json_obj)
    return access_token


def validate_and_get_provider(request):
    provider_name, _ = get_state(request)
    try:
        dp = DataProvider.objects.get(provider_name=provider_name)
        return DataProviderO(dp.data_provider_instance.pk)
    except ObjectDoesNotExist as e:
        logger.error(str(e))
        raise OauthRedirectRequestException(
            "state did not return a valid data provider object. provider: %s" % provider_name)


def get_state(request):
    state = request.GET.get('state') or request.POST.get('state')
    if not state or ":" not in state:
        raise OauthRedirectRequestException("state was not parsed or invalid. state: %s" % str(state))
    return state.split(":")


def get_scope(request):
    return request.GET.get('scope') or request.POST.get('scope')


def get_auth_code(request):
    code = request.GET.get('code') or request.POST.get('code')
    return code


def validate_and_get_profile(request):
    _, user_id = get_state(request)
    if not hasattr(request.user, "profile") or request.user.pk is None:
        raise OauthRedirectRequestException("you are not logged in")
    profile_on_user = request.user.profile
    profile_by_id = Profile.objects.get(user__pk=user_id)

    if profile_on_user.pk != profile_by_id.pk:
        raise OauthRedirectRequestException("logged in profile do not match with the state")
    return profile_on_user


def save_data_provider_profile(access_token, data_provider, profile):
    try:
        tpp = DataProviderProfile.objects.get(
            profile=profile, provider=data_provider.db_data_provider)
        tpp.access_token = access_token
    except ObjectDoesNotExist:
        tpp = DataProviderProfile(
            provider=data_provider.db_data_provider,
            access_token=access_token,
            profile=profile
        )

    tpp.save()

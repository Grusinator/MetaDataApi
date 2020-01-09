import logging

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from MetaDataApi.utils import JsonUtils
from dataproviders.models import DataProviderUser, DataProvider


class OauthRedirectRequestException(Exception):
    pass


logger = logging.getLogger(__name__)


def handle_oath_redirect(request):
    code = get_auth_code(request)
    scope = get_scope(request)
    user = validate_and_get_user(request)
    data_provider = validate_and_get_provider(request)
    access_token_content = request_access_token(code, data_provider)
    data_provider_user = update_or_create_data_provider_user(access_token_content, data_provider, user)
    return data_provider_user


def refresh_access_token(data_provider_user: DataProviderUser):
    data = build_refresh_access_token_data(data_provider_user)
    url = data_provider_user.data_provider.oauth_config.access_token_url
    r = requests.post(url, data=data, allow_redirects=True)
    if not r.ok:
        raise OauthRedirectRequestException("the token request did not return with ok. Reason: %s" % r.reason)
    response_content = JsonUtils.validate(r.content)
    access_token = response_content.get("access_token")
    update_or_create_data_provider_user(response_content, data_provider_user.data_provider, data_provider_user.user)


def build_refresh_access_token_data(data_provider_user: DataProviderUser):
    return {
        "grant_type": "refresh_token",
        "refresh_token": data_provider_user.refresh_token,
        "client_id": data_provider_user.data_provider.oauth_config.client_id,
        "client_secret": data_provider_user.data_provider.oauth_config.client_secret,
    }


def request_access_token(code, data_provider):
    data = build_request_access_token_data(code, data_provider)
    url = data_provider.oauth_config.access_token_url
    r = requests.post(url, data=data, allow_redirects=True)
    if not r.ok:
        raise OauthRedirectRequestException("the token request did not return with ok. Reason: %s" % r.reason)
    response_content = JsonUtils.validate(r.content)
    access_token = response_content.get("access_token")
    if access_token is "" or None:
        raise OauthRedirectRequestException("access token was not found in response: %s" % response_content)
    return response_content


def build_request_access_token_data(code, data_provider):
    return {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": data_provider.oauth_config.client_id,
        "client_secret": data_provider.oauth_config.client_secret,
        "redirect_uri": settings.OAUTH_REDIRECT_URI,
    }


def validate_and_get_provider(request):
    provider_name, _ = get_state(request)
    try:
        return DataProvider.objects.get(provider_name=provider_name)
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


def validate_and_get_user(request):
    state_user = get_user_from_oauth_state(request)
    return state_user


def get_user_from_oauth_state(request):
    _, user_id = get_state(request)
    user = User.objects.get(pk=user_id)
    return user


def validate_user_has_profile(user):
    if hasattr(user, "profile"):
        return user.profile
    else:
        raise OauthRedirectRequestException("user do not have a profile")


def update_or_create_data_provider_user(access_token_content, data_provider, user):
    keys = ('access_token', 'token_type', 'refresh_token', 'expires_in')
    defaults = {key: access_token_content[key] for key in keys if key in access_token_content}
    dpu, _ = DataProviderUser.objects.update_or_create(user=user, data_provider=data_provider, defaults=defaults)
    return dpu

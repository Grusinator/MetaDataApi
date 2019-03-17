import json
import logging

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from dataproviders.models import ThirdPartyDataProvider
from settings import OAUTH_REDIRECT_URI
from users.models import Profile
from users.models import ThirdPartyProfile

logger = logging.getLogger(__name__)

# Create your views here.


def data_provider_list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    data_providers = ThirdPartyDataProvider.objects.all()

    return render(request, 'dataproviders.html',
                  {
                      "dataproviders": data_providers,
                      "user_id": request.user.pk
                  })


def provider_list_view(ListView):
    queryset = ThirdPartyDataProvider.objects.all()


def oauth2redirect(request):
    # if not request.user.is_authenticated:
    #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    try:
        code = request.GET.get('code') or request.POST.get('code')
        scope = request.GET.get('scope') or request.POST.get('scope')
        state = request.GET.get('state') or request.POST.get('state')

        provider_name, user_id = state.split(":")

        data_provider = ThirdPartyDataProvider.objects.get(
            provider_name=provider_name)

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": data_provider.client_id,
            "client_secret": data_provider.client_secret,
            "redirect_uri": OAUTH_REDIRECT_URI,
        }

        url = data_provider.access_token_url
        r = requests.post(url, data=data, allow_redirects=True)

        json_obj = json.loads(r.content)

        errors = json_obj.get("errors")
        if errors:
            raise Exception(str(errors))

        access_token = json_obj.pop("access_token")
        token_type = json_obj.pop("token_type")

        try:
            profile = request.user.profile
        except:
            profile = Profile.objects.get(user__pk=user_id)

        try:
            tpp = ThirdPartyProfile.objects.get(
                profile=profile, provider=data_provider)
            tpp.access_token = access_token
        except:
            tpp = ThirdPartyProfile(
                provider=data_provider,
                access_token=access_token,
                profile=profile,
                profile_json_field=json_obj
            )

        tpp.save()

        return HttpResponse(
            """successfully connected your profile with %s
            <a href= "%s"> back <a> """
            % (provider_name,
                "../providers/")
        )

    except Exception as e:
        logger.error(e)
        return HttpResponse("upps... something went wrong! (%s)" % str(e))

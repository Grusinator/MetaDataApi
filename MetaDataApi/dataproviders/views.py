from django.shortcuts import render
from MetaDataApi.dataproviders.models import ThirdPartyDataProvider
from MetaDataApi.users.models import ThirdPartyProfile
import json
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import ListView

from MetaDataApi.users.models import Profile
# Create your views here.


def data_provider_list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    data_providers = ThirdPartyDataProvider.objects.all()

    return render(request, 'dataproviders.html',
                  {"dataproviders": data_providers})


def provider_list_view(ListView):
    queryset = ThirdPartyDataProvider.objects.all()


def oauth2redirect(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    try:
        code = request.GET.get('code') or request.POST.get('code')
        scope = request.GET.get('scope') or request.POST.get('scope')
        state = request.GET.get('state') or request.POST.get('state')

        provider_name, user_id = state.split(":")

        dp = ThirdPartyDataProvider.objects.get(provider_name=provider_name)

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": dp.client_id,
            "client_secret": dp.client_secret,
            "redirect_uri": dp.redirect_uri,
        }

        url = dp.access_token_url
        r = requests.post(url, data=data, allow_redirects=True)

        json_obj = json.loads(r.content)

        errors = json_obj.get("errors")
        if errors:
            raise Exception(str(errors))

        access_token = json_obj.pop("access_token")
        token_type = json_obj.pop("token_type")

        try:
            profile = request.user.profile,
        except:
            profile = Profile.objects.get(user__pk=user_id)

        tpp = ThirdPartyProfile(
            provider=dp,
            access_token=access_token,
            profile=profile,
            profile_json_field=json_obj
        )
        tpp.save()

        return HttpResponse("""successfully connected your profile with %s
                            <a href= "http://localhost:8000/provider/"> back <a> """
                            % state)
    except Exception as e:
        return HttpResponse("upps... something went wrong! (%s)" % str(e))

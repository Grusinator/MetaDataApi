from django.shortcuts import render
from MetaDataApi.dataproviders.models import ThirdPartyDataProvider
from MetaDataApi.users.models import ThirdPartyProfile
import json
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
# Create your views here.


def data_provider_list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    data_providers = ThirdPartyDataProvider.objects.all()

    return render(request, 'dataproviders.html',
                  {"dataproviders": data_providers})


def oauth2redirect(request):
    try:
        code = request.GET.get('code')
        scope = request.GET.get('scope')
        state = request.GET.get('state')

        dp = ThirdPartyDataProvider.objects.get(provider_name=state)

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

        tpp = ThirdPartyProfile(
            provider=dp,
            access_token=access_token,
            profile=request.user.profile,
            profile_json_field=json_obj
        )
        tpp.save()

        return HttpResponse("successfully connected your profile with %s"
                            % state)
    except Exception as e:
        return HttpResponse("upps... something went wrong! (%s)" % str(e))

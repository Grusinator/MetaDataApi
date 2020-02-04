from django.http import HttpResponse

from dataproviders.services.oauth import handle_oath_redirect


def oauth2redirect_view(request):
    data_provider_user = handle_oath_redirect(request)
    return HttpResponse(
        """successfully connected your profile with %s
        <a href= "%s"> back <a> """
        % (data_provider_user.data_provider.provider_name,
           "../providers/")
    )



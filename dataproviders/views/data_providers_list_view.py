import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from dataproviders.models import DataProvider

logger = logging.getLogger(__name__)


@login_required
def data_provider_list_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    data_providers = DataProvider.objects.all()

    return render(request, 'dataproviders.html',
                  {
                      "dataproviders": data_providers,
                      "user_id": request.user.pk,
                  })

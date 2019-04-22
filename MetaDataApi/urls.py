"""MetaDataApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from graphene_django.views import GraphQLView

from MetaDataApi.dataproviders.views import DataProviderView, oauth2redirect_view
from MetaDataApi.dataproviders.views.endpoint_detail_view import endpoint_detail_view
from MetaDataApi.dataproviders.views.object_view import object_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        'providers/',
        DataProviderView.data_provider_list,
        name='providers'
    ),
    path(
        'provider/<str:provider_name>',
        DataProviderView.data_provider,
        name='provider_detail'),
    path(
        'provider/<str:provider_name>/endpoint/<str:endpoint_name>',
        endpoint_detail_view,
        name='endpoint_detail'
    ),
    path(
        'provider/<str:provider_name>/object/<str:object_label>',
        object_view,
        name='objects'
    ),
    url(r'^oauth2redirect/$', oauth2redirect_view, name='oauth2redirect'),
    url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
    url(r'^$', RedirectView.as_view(
        url='accounts/login?next=/providers/', permanent=False), name='login')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

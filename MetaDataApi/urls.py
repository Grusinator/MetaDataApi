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

from MetaDataApi.dataproviders.views import data_provider_list, oauth2redirect

# from graphene_file_upload.django import FileUploadGraphQLView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('providers/', data_provider_list, name='providers'),
    # path("provider_list", provider_list_view.as_view(), name='provider_list'),
    url(r'^oauth2redirect/$', oauth2redirect, name='oauth2redirect'),
    url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
    url(r'^$', RedirectView.as_view(
        url='accounts/login?next=/providers/', permanent=False), name='login')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

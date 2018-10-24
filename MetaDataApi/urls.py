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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from graphene_django.views import GraphQLView

from django.conf.urls.static import static
from django.conf import settings


from django.views.generic.base import RedirectView
from MetaDataApi.dataproviders.views import data_provider_list

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('results/', data_provider_list, name='results'),
    url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
    url(r'^$', RedirectView.as_view(url='admin/', permanent=False), name='admin')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

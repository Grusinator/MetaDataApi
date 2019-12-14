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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from app.views import admin_view
from dataproviders.views import oauth2redirect_view

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'admin_i/', admin_view),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('dynamic_models/', include('MetaDataApi.dynamic_models.urls')),
    path("providers/", include('dataproviders.urls')),
    url(r'^oauth2redirect/$', oauth2redirect_view, name='oauth2redirect'),
    # url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
    url(r'^$', RedirectView.as_view(url='accounts/login?next=/providers/', permanent=False), name='login'),
    # path('', include('social_django.urls', namespace='social')),
    # path('logout/', logout, name='logout'),

]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

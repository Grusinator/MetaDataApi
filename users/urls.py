from django.conf.urls import url
from django.contrib.auth import logout
from django.urls import path, include

from users.views import signup_view

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', signup_view, name='signup'),
    # path('', include('social_django.urls', namespace='social')),
    url('logout/', logout, {'next_page': '/'}, name='logout'),
]

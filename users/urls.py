from django.conf.urls import url
from django.contrib.auth import logout, login
from django.urls import path, include

from users.views import signup_view

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('', include('social_django.urls', namespace='social')),
    url('signup/', signup_view, name='signup'),
    url('logout/', logout, {'next_page': '/'}, name='logout', ),
    url('login/', login, {'next_page': '/'}, name='login')
]

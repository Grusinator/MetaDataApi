from django.contrib import admin

# Register your models here.
from MetaDataApi.users.models import Profile, ThirdPartyProfile

from MetaDataApi.metadata.services import *
admin.site.register(Profile)

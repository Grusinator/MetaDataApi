from django.contrib import admin

# Register your models here.
from MetaDataApi.users.models import Profile, ThirdPartyProfile

admin.site.register(Profile)
admin.site.register(ThirdPartyProfile)

from django.contrib import admin

# Register your models here.
from MetaDataApi.users.models import Profile

admin.site.register(Profile)

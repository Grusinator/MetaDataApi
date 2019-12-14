from django.contrib import admin

# Register your models here.
from users.models.profile import Profile

admin.site.register(Profile)

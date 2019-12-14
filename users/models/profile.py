from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class Languages(Enum):
    Danish = "dk"
    English = "en"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    language = models.TextField(
        blank=False, max_length=2,
        choices=[(tag.value, tag.name) for tag in Languages],
        default=Languages.Danish
    )
    profilepicture = models.ImageField(
        upload_to='profilepictures', null=True, blank=True)
    profile_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%i - %s - %s" % (self.id, self.user.username, self.language)

    class Meta:
        app_label = 'users'
        default_related_name = 'profile'

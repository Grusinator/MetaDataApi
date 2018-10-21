from django.db import models
from django.conf import settings
from enum import Enum

# Create your models here.


class Languages(Enum):
    Danish = "dk"
    English = "en"

class Profile(models.Model):
    birthdate = models.DateField(null=True, blank=True)
    language = models.TextField(blank=False, max_length=2,
        choices=[(tag.value, tag.name) for tag in Languages])
    profilepicture = models.ImageField(upload_to='profilepictures', null=True, blank=True)
    audio_threshold = models.FloatField(null=True,blank=True)
    profile_description = models.TextField(blank=True)
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return "%i - %s - %s"%(self.id, self.user.username,  self.language)

    class Meta:
        app_label = 'users'

class ThirdPartyProfile(models.Model):
    provider = models.TextField(null=False, blank=False) # consider if this shoud be a foreignkey to provider or enum
    profile = models.ForeignKey(Profile, null=False, on_delete=models.CASCADE)
    access_token = models.TextField(null=False, blank = False)
    profile_json_field = models.TextField(null=False,blank = False)

    def __str__(self):
        return "%s - %s"%(self.provider, self.profile.user.username)

    class Meta:
        app_label = 'users'

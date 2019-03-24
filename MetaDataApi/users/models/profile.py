from enum import Enum

from django.contrib.auth.models import User
from django.db import models

from MetaDataApi.metadata.models import ObjectInstance, Object


class Languages(Enum):
    Danish = "dk"
    English = "en"


class Profile(models.Model):
    birthdate = models.DateField(null=True, blank=True)
    language = models.TextField(
        blank=False, max_length=2,
        choices=[(tag.value, tag.name) for tag in Languages])
    profilepicture = models.ImageField(
        upload_to='profilepictures', null=True, blank=True)
    audio_threshold = models.FloatField(null=True, blank=True)
    profile_description = models.TextField(null=True, blank=True)
    foaf_person = models.ForeignKey(
        "metadata.ObjectInstance",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%i - %s - %s" % (self.id, self.user.username, self.language)

    def get_data_provider_profile(self, provider_name):
        tpdp_profile = self.data_provider_profiles.get(
            provider__provider_name=provider_name)
        return tpdp_profile

    def save(self, *args, **kwargs):
        person_meta = Object.objects.get(schema__label="friend_of_a_friend", label="person")
        person_instance = ObjectInstance(base=person_meta)
        person_instance.save()
        self.foaf_person = person_instance

        super(Profile, self).save(*args, **kwargs)

    class Meta:
        app_label = 'users'
        default_related_name = 'profile'

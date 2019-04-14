from django.db import models


class DataProviderProfile(models.Model):
    # consider if this shoud be a foreignkey to provider or enum
    provider = models.ForeignKey(
        'dataproviders.DataProvider', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', related_name="data_provider_profiles",
                                null=False, on_delete=models.CASCADE)
    access_token = models.TextField(null=False, blank=False)
    profile_json_field = models.TextField(null=False, blank=False)

    def __str__(self):
        return "%s - %s" % (self.provider, self.profile.user.username)

    class Meta:
        unique_together = ('provider', 'profile')
        app_label = 'users'

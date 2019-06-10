from django.db import models


class DataProviderProfile(models.Model):
    data_provider = models.ForeignKey(
        'dataproviders.DataProvider', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', related_name="data_provider_profiles",
                                null=False, on_delete=models.CASCADE)
    access_token = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.data_provider} - {self.profile.user.username}"

    class Meta:
        unique_together = ('data_provider', 'profile')
        app_label = 'users'

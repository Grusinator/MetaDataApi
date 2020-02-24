from django.contrib.auth.models import User
from django.db import models
from djcelery_model.models import TaskMixin

from dataproviders.models import DataProvider

data_provider_user_save_methods = []


class DataProviderUser(TaskMixin, models.Model):
    data_provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(null=True, blank=True, max_length=255)
    token_type = models.CharField(null=True, blank=True, max_length=32)
    expires_in = models.IntegerField(null=True, blank=True)

    data_fetching_is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.data_provider} - {self.user.username}"

    class Meta:
        unique_together = ('data_provider', 'user')
        app_label = 'dataproviders'
        default_related_name = "data_provider_users"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.execute_on_save_methods()

    def execute_on_save_methods(self):
        for method in data_provider_user_save_methods:
            method(self)

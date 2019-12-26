from django.contrib.auth.models import User
from django.db import models
from djcelery_model.models import TaskMixin

from dataproviders.tasks import fetch_data_from_provider_endpoint


class DataProviderUser(TaskMixin, models.Model):
    data_provider = models.ForeignKey(
        'dataproviders.DataProvider', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="data_provider_users", null=False, on_delete=models.CASCADE)
    access_token = models.TextField(null=False, blank=False)

    data_fetching_is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.data_provider} - {self.user.username}"

    class Meta:
        unique_together = ('data_provider', 'user')
        app_label = 'dataproviders'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_or_update_endpoint_tasks()

    def create_or_update_endpoint_tasks(self):
        if self.data_fetching_is_active:
            endpoints = self.data_provider.endpoints.all()
            for endpoint in endpoints:
                # TODO make sure that the task is not created many times
                self.apply_async(fetch_data_from_provider_endpoint, self.data_provider.provider_name,
                                 endpoint.endpoint_name, self.user.pk)

from django.contrib.auth.models import User
from django.db import models
from djcelery_model.models import TaskMixin


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

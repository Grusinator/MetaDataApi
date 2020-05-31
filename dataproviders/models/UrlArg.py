from django.db import models

from dataproviders.models import Endpoint
from dataproviders.models.UrlArgFormatter import UrlArgFormatter
from dataproviders.models.UrlArgType import UrlArgType


class UrlArg(models.Model):
    endpoint = models.ForeignKey(Endpoint, related_name="url_args", on_delete=models.CASCADE)
    key_name = models.CharField(max_length=50)
    arg_type = models.CharField(max_length=50, choices=UrlArgType.build_choices())
    value_formatter = models.CharField(choices=UrlArgFormatter.build_choices(), null=True, blank=True,
                                       default=UrlArgFormatter.NONE.value,
                                       max_length=50)

    def __str__(self):
        return f"{self.endpoint.endpoint_name} - {self.key_name}={self.arg_type}"

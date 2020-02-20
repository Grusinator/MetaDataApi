from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from generic_serializer import SerializableModel


class DataProvider(models.Model, SerializableModel):
    icon_image_url = models.URLField(null=True, blank=True)
    # icon_image = models.ImageField(null=True, blank=True)
    provider_name = models.TextField(unique=True)
    provider_url = models.URLField(null=True, blank=True)
    api_endpoint = models.TextField(null=True, blank=True)

    def get_internal_view_url(self):
        return reverse('provider_detail', args=[str(self.provider_name)])

    # def get_webvowl_url(self):
    #     schema = self.get_schema_for_provider()
    #     return "http://visualdataweb.de/webvowl/#iri=" + schema.rdfs_file.url

    def __str__(self):
        return "%s - %s" % (self.provider_name, self.api_endpoint)

    def save(self, *args, **kwargs):
        # if not Schema.exists_by_label(str(self.provider_name)):
        #     pass
        #     # TODO add back in: Schema.create_new_empty_schema(self.provider_name)

        super(DataProvider, self).save(*args, **kwargs)

    @classmethod
    def exists(cls, provider_name):
        try:
            return cls.objects.get(provider_name=provider_name)
        except ObjectDoesNotExist:
            return None

    class Meta:
        app_label = 'dataproviders'

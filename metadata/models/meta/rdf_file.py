from django.db import models

from MetaDataApi.custom_storages import PrivateMediaStorage


class RDFDataDump(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    rdf_file = models.FileField(
        upload_to='datapoints/audio', storage=PrivateMediaStorage())
    schema = models.ForeignKey('Schema', related_name='data_dumps', on_delete=models.CASCADE)

    class Meta:
        app_label = 'metadata'

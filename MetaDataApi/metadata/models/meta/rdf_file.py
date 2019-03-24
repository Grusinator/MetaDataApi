from django.db import models

from MetaDataApi.metadata.custom_storages import MediaStorage


class RDFDataDump(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    rdf_file = models.FileField(
        upload_to='datapoints/audio', storage=MediaStorage())
    schema = models.ForeignKey('Schema', related_name='data_dumps', on_delete=models.CASCADE)

    class Meta:
        app_label = 'metadata'

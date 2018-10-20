from django.contrib import admin

# Register your models here.
from MetaDataApi.datapoints.models import DatapointV2, MetaData, RawData

list = [DatapointV2, MetaData, RawData]
for model in list:
    admin.site.register(model)

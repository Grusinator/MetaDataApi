import json
from django import forms

from service_objects.services import Service

from MetaDataApi.metadata.services import *

from MetaDataApi.metadata.models import *
from django.contrib.auth.models import User


from MetaDataApi.dataproviders.services import DataProviderEtlService


class GetTemporalFloatPairsService(Service):
    schema_label = forms.CharField()
    object_label = forms.CharField()
    attribute_label = forms.CharField()
    datetime_label = forms.CharField()

    def process(self):
        schema_label = self.cleaned_data['schema_label']
        object_label = self.cleaned_data['object_label']
        attribute_label = self.cleaned_data['attribute_label']
        datetime_label = self.cleaned_data['datetime_label']

        value_att = Attribute.objects.get(
            label=attribute_label,
            object__label=object_label,
            object__schema__label=schema_label)

        if datetime_label:
            datetime_att = Attribute.objects.get(
                label=datetime_label,
                object__label=object_label,
                object__schema__label=schema_label
            )
        else:
            datetime_att = identify()

        get_connected_attribute_pairs(value_Att, datetime_att)

        data =

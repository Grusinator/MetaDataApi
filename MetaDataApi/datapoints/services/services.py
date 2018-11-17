import json
from django import forms

from service_objects.services import Service

from MetaDataApi.metadata.services import *

from MetaDataApi.metadata.models import *
from MetaDataApi.metadata.models import *

from django.contrib.auth.models import User

from datetime import datetime


from MetaDataApi.dataproviders.services import DataProviderEtlService


# class GetTemporalFloatPairsService(Service):
#     schema_label = forms.CharField()
#     object_label = forms.CharField()
#     attribute_label = forms.CharField()
#     datetime_label = forms.CharField(required=False)
#     datetime_object_label = forms.CharField(required=False)

#     def process(self):
#         schema_label = self.cleaned_data['schema_label']
#         object_label = self.cleaned_data['object_label']
#         attribute_label = self.cleaned_data['attribute_label']
#         datetime_label = self.cleaned_data['datetime_label']
#         datetime_object_label = self.cleaned_data['datetime_object_label']

#         value_att = Attribute.objects.get(
#             label=attribute_label,
#             object__label=object_label,
#             object__schema__label=schema_label)

#         Attribute.assert_data_type(value_att, float)

#         if datetime_label:
#             datetime_att = Attribute.objects.get(
#                 label=datetime_label,
#                 object__label=datetime_object_label or object_label,
#                 object__schema__label=schema_label
#             )
#             Attribute.assert_data_type(datetime_att, datetime)

#         else:
#             raise NotImplementedError(
#                 "identify not implemented, specify a secondary label")
#             datetime_att = identify()

#         service = BaseMetaDataService()
#         data = service.get_connected_attribute_pairs(value_att, datetime_att)

#         # data_values = [(att_inst1.value, att_inst2.value)
#         #                for att_inst1, att_inst2 in data]

#         return data

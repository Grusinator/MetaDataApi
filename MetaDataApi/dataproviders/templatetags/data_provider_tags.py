import json

from django import template

from MetaDataApi.dataproviders.models import DataProvider

register = template.Library()


@register.filter(name='load_json')
def load_json(value):
    try:
        return json.loads(value)
    except:
        return []


@register.simple_tag
def build_auth_url(data_provider: DataProvider, user_id):
    return data_provider.build_auth_url(user_id)

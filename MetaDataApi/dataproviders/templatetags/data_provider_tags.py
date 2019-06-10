import json

from django import template

register = template.Library()


@register.filter(name='load_json')
def load_json(value):
    try:
        return json.loads(value)
    except:
        return []



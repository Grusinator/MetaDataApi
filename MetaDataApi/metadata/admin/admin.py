from django.contrib import admin

# Register your models here.
from metadata.models import *

models = (
    # instances
    RawData,)


[admin.site.register(model) for model in models]

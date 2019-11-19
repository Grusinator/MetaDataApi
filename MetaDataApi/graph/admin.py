# Register your models here.
from django.contrib import admin
from mutant import models

from MetaDataApi.graph.models import Dummy

admin.site.register(Dummy)

admin.site.register(models.FieldDefinition)

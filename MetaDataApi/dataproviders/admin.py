from django.contrib import admin

# Register your models here.
from MetaDataApi.dataproviders.models import ThirdPartyDataProvider

models = (ThirdPartyDataProvider,)

[admin.site.register(model) for model in models]

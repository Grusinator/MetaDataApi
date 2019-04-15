from django.apps import AppConfig


class DataprovidersConfig(AppConfig):
    name = 'MetaDataApi.dataproviders'

    def ready(self):
        from MetaDataApi.dataproviders.models.load_default_data_providers import InitializeDefaultDataProviders
        InitializeDefaultDataProviders.load()

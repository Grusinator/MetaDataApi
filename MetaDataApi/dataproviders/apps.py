from django.apps import AppConfig


class DataprovidersConfig(AppConfig):
    name = 'MetaDataApi.dataproviders'

    def ready(self):
        try:
            from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders
            # if not settings.DEBUG | True:
            InitializeDataProviders.load()
        except Exception as e:
            print(f"could not initialize data providers due to error {e}")

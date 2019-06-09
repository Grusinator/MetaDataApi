from django.apps import AppConfig


class MetadataConfig(AppConfig):
    name = 'MetaDataApi.metadata'

    def ready(self):
        try:
            from MetaDataApi.metadata.models import Schema
            if not Schema.exists_by_label("friend_of_a_friend"):
                from MetaDataApi.metadata.tests import LoadTestData
                LoadTestData.init_foaf()
        except Exception:
            print("could not load foaf")

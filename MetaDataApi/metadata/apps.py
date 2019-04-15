from django.apps import AppConfig


class MetadataConfig(AppConfig):
    name = 'MetaDataApi.metadata'

    def ready(self):
        from MetaDataApi.metadata.rdfs_models.initialize_rdf_models import InitializeRdfModels
        InitializeRdfModels.create_all_schemas()
        from MetaDataApi.metadata.tests import LoadTestData
        LoadTestData.init_foaf()

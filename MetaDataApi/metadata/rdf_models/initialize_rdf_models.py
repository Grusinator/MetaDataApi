from . import RdfDataProvider


class InitializeRdfModels:
    rdf_models = [RdfDataProvider]

    @classmethod
    def create_all_schemas(cls):
        for rdf_model in cls.rdf_models:
            if not rdf_model.do_schema_items_exists():
                rdf_model.create_all_meta_objects()

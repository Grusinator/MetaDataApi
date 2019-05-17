from . import RdfsDataProvider


class InitializeRdfModels:
    rdf_models = [RdfsDataProvider]

    @classmethod
    def create_all_schemas(cls):
        for rdf_model in cls.rdf_models:
            if not rdf_model.do_schema_items_exists():
                rdf_model.create_all_meta_objects()

    @classmethod
    def create_all_schemas_from_descriptor(cls):
        for rdf_model in cls.rdf_models:
            for rdf_object in rdf_model.SchemaObjects:
                rdf_object.initialize_schema()

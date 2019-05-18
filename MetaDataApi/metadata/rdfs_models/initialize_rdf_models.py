from . import RdfsDataProvider


class InitializeRdfModels:
    rdf_models = [RdfsDataProvider]

    initialized_objects = []
    pending_relations = []

    @classmethod
    def create_all_schemas(cls):
        for rdf_model in cls.rdf_models:
            if not rdf_model.do_schema_items_exists():
                rdf_model.create_all_meta_objects()

    @classmethod
    def create_all_schemas_from_descriptor(cls):
        for rdf_model in cls.rdf_models:
            for rdf_object in rdf_model.SchemaObjects:
                if rdf_object not in cls.initialized_objects:
                    rdf_object.initialize_schema_objects()

        for rdf_model in cls.rdf_models:
            for rdf_object in rdf_model.SchemaObjects:
                cls.pending_relations.extend(rdf_object.initialize_object_relations())
        cls.delete_confirmed_pending()

    @classmethod
    def delete_confirmed_pending(cls):
        for pending_rel in list(cls.pending_relations):
            reverse = reversed(pending_rel)
            if reverse in cls.pending_relations:
                cls.pending_relations.remove(reverse)
                cls.pending_relations.remove(pending_rel)

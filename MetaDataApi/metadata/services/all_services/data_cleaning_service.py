from MetaDataApi.metadata.models import (
    SchemaNode, SchemaEdge
)
from .base_functions import BaseMetaDataService


class DataCleaningService(BaseMetaDataService):

    def __init__(self, *args, **kwargs):
        super(DataCleaningService, self).__init__()

    def relate_root_classes_to_foaf(self, schema):
        foaf = self.get_foaf_person()

        self.schema = schema

        root_objects = SchemaNode.objects.filter(
            from_edge=None,
            schema=self.schema
        )
        for obj in root_objects:
            label = "person_has_%s" % obj.label
            self._try_create_meta_item(
                SchemaEdge(
                    from_object=foaf,
                    to_object=obj,
                    schema=self.schema,
                    label=label
                )
            )
        return self.touched_meta_items

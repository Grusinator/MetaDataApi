from .base_functions import BaseMetaDataService
from MetaDataApi.metadata.models import (
    Schema, Object, ObjectRelation, Attribute
)


class DataCleaningService(BaseMetaDataService):

    def __init__(self, *args, **kwargs):
        super(DataCleaningService, self).__init__()

    def relate_root_classes_to_foaf(self, schema_label):
        foaf = self.get_foaf_person()

        schema = Schema.objects.get(label=schema_label)
        root_objects = Object.objects.filter(
            from_relations=None,
            schema=schema
        )
        for obj in root_objects:
            label = "person_has_%s" % obj.label
            self._try_create_item(
                ObjectRelation(
                    from_object=foaf,
                    to_object=obj,
                    schema=schema,
                    label=label
                )
            )
        return self._objects_created_list

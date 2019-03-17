import logging

from django.contrib.auth.models import User

from metadata.models import (
    ObjectInstance)
from metadata.services.all_services.base_functions import BaseMetaDataService
from metadata.utils.django_model_utils.build_data_objects_from_json import BuildDataObjectsFromJson

# Get an instance of a logger
logger = logging.getLogger(__name__)


class JsonAnalyser:
    def __init__(self):
        self.meta_data_list = []
        self.schema = None
        self.owner = None

        self._att_function = None
        self._object_function = None
        self._obj_rel_function = None

    def identify_from_json_data(self, input_data, schema, owner: User, parrent_label=None):
        # setup how the loop handles each type of object occurrence

        builder = BuildDataObjectsFromJson(schema, owner)

        person = ObjectInstance(
            base=BaseMetaDataService.get_foaf_person()
        )
        person.save()
        # TODO: Relate to logged in foaf person object instance instead

        input_data = self._inject_parrent_label_as_root_key(input_data, parrent_label)

        builder.build_from_json(input_data, parrent_object=person)

        return builder.added_instance_items

    @staticmethod
    def _inject_parrent_label_as_root_key(input_data, parrent_label):
        if parrent_label is not None and isinstance(input_data, list):
            # if its a list, we have to create a base object for each element
            input_data = [{parrent_label: elm} for elm in input_data]
        elif parrent_label is not None and isinstance(input_data, dict):
            # if its a dict, just add the parrent label
            input_data = {parrent_label: input_data, }
        return input_data

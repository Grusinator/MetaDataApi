import logging
from abc import ABCMeta, abstractmethod

from json2model.services.dynamic_model.failed_object import FailedObject

logger = logging.getLogger(__name__)


class IJsonIterator:
    __metaclass__ = ABCMeta

    JSON_ATTRIBUTE_TYPES = (str, int, float, bool)

    def __init__(self):
        self.failed_objects = []

    @abstractmethod
    def handle_attribute(self, object_ref: str, attribute_label: str, data):
        """This method is for dealing with each attribute that gets identified in the tree including lists of
        attributes"""
        raise NotImplementedError

    @abstractmethod
    def pre_handle_object(self, parent_ref: str, object_label: str, data):
        """do what ever you must with the current object that has been identified, what ever is returned here will
        be passed along as object ref in the other methods"""
        raise NotImplementedError

    @abstractmethod
    def post_handle_object(self, parent_ref: str, object_ref: str, data):
        """do what ever you must with the current object, but after creation of the relation and attributes.
        implement it as "return object_ref" if no other functionality is needed"""
        logger.info("post_handle_object method has no implementation")
        return object_ref

    @abstractmethod
    def handle_related_object(self, parent_ref: str, related_object_ref: str, object_label,
                              parent_has_many: bool = False):
        """This method is called after exiting the iteration of the related object, so the relation can be handled
        after both objects has been handled"""
        raise NotImplementedError

    @abstractmethod
    def do_rollback_on_error(self, parent_ref: str, object_label: str, data):
        """If the pre_handle_object, handle_attribute and post_handle_object fails, this method can be used to undo the
         things that was made"""
        logger.info("do_rollback_on_error method has no implementation")

    def _iterate_data_structure(self, data, object_label=None, parent_ref=None):
        if isinstance(data, list):
            return "Why is this a list"
        attributes, one2one_related_objs, one2many_related_objs = self._split_into_attributes_and_related_objects(data)
        try:
            object_ref = self.handle_object_and_attributes(parent_ref, object_label, data, attributes)
        except Exception as e:
            self.do_rollback_on_error(parent_ref, object_label, data)
            logger.error(f"object: {object_label}, could not be created due to error: {e}")
            failed_object = FailedObject(object_label, e, data)
            self.failed_objects.append(failed_object)
            return failed_object
        else:
            self.try_handle_related_objects(object_ref, one2many_related_objs, one2one_related_objs)
            return object_ref

    def try_handle_related_objects(self, object_ref, one2many_related_objs, one2one_related_objs):
        try:
            self._handle_one2one_related_objects(object_ref, one2one_related_objs)
            self._handle_one2many_related_objects(object_ref, one2many_related_objs)
        except Exception as e:
            logger.error(f"related objects to object: {object_ref}, could not be created due to error: {e}")

    def handle_object_and_attributes(self, parent_ref, object_label, data, attributes: dict):
        object_ref = self.pre_handle_object(parent_ref, object_label, data)
        self._handle_attributes(object_ref, attributes)
        object_ref = self.post_handle_object(parent_ref, object_ref, data)
        return object_ref

    def _handle_attributes(self, object_ref, data: dict):
        return [self.handle_attribute(object_ref, label, data) for label, data in data.items()]

    def _handle_one2one_related_objects(self, parent_ref, data):
        return {label: self._inner_handle_related_object(parent_ref, label, inner_data) for label, inner_data in
                data.items()}

    def _handle_one2many_related_objects(self, parent_ref, data):
        for related_label, objects in data.items():
            for object_data in objects:
                self._inner_handle_related_object(parent_ref, related_label, object_data, parent_has_many=True)

    def _inner_handle_related_object(self, parent_ref, object_label: str, data, parent_has_many: bool = False):
        related_object_ref = self._iterate_data_structure(data, object_label=object_label, parent_ref=parent_ref)
        self.handle_related_object(parent_ref, related_object_ref, object_label, parent_has_many=parent_has_many)
        return related_object_ref

    def _split_into_attributes_and_related_objects(self, data):
        properties = {}
        one2one_related_objects = {}
        one2many_related_objects = {}
        for name, value in data.items():
            # only one2one relations are selected here
            if isinstance(value, dict):
                one2one_related_objects[name] = value
            # if it is a list it will either be an attribute or a one2many relation, and we dont deal with that here.
            elif isinstance(value, list):
                if not any(self.list_element_is_objects(
                        value)):  # and all([type(val) in ATTRIBUTE_TYPES for val in value]):
                    properties[name] = value
                elif all(self.list_element_is_objects(value)):
                    one2many_related_objects[name] = value
                else:
                    raise NotImplementedError("i dont know what kind of obscure mixed types of lists can occur "
                                              "(fx objects and values)")
            elif isinstance(value, self.JSON_ATTRIBUTE_TYPES):
                properties[name] = value
            elif value is None:
                logger.debug(f"property {name} has value {value} which is excluded")
            else:
                raise NotImplementedError("the list contains not known attribute data types")
        return properties, one2one_related_objects, one2many_related_objects

    def list_element_is_objects(self, data):
        return list(map(lambda x: isinstance(x, dict), data))

    def start_iterating_data_structure(self, data, root_label):
        if isinstance(data, list):
            object_name = self._start_iterating_as_list(root_label, data)
        elif isinstance(data, dict):
            object_name = self._iterate_data_structure(data, object_label=root_label)
        else:
            raise NotImplementedError("cant handle other datatypes")
        return object_name

    def _start_iterating_as_list(self, root_label, data):
        objects = [self._iterate_data_structure(data_elm, object_label=root_label) for data_elm in data]
        return objects

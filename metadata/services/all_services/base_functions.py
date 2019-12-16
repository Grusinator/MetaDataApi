import logging
from datetime import datetime

from django.core.exceptions import (
    ObjectDoesNotExist, MultipleObjectsReturned)
from django.db import transaction

from MetaDataApi.utils.common_utils import StringUtils
from metadata.models import (
    Node, Edge,
    StringAttribute,
    DateTimeAttribute, BoolAttribute,
    FloatAttribute, IntAttribute
)
# from jsonschema import validate
from metadata.models import (
    Schema, SchemaNode, SchemaAttribute, SchemaEdge)

logger = logging.getLogger(__name__)


class BaseMetaDataService:
    att_inst_to_type_map = {
        #  StringAttribute: str,
        StringAttribute: str,
        DateTimeAttribute: datetime,
        FloatAttribute: float,
        IntAttribute: int,
        BoolAttribute: bool
    }

    def __init__(self):
        self.schema = None

        self.added_meta_items = []
        self.touched_meta_items = []
        self.added_instance_items = []
        self._error_list = []
        # one switch to force overwrite the objects when
        self.overwrite_db_objects = False
        # -- same -- but to disable saving to db
        self.save_to_db = True

        self.att_types = tuple(typ if isinstance(typ, type) else type(typ)
                               for typ in SchemaAttribute.data_type_map.keys())

        self.att_instances = tuple(self.att_inst_to_type_map.keys())

        self.instances = self.att_instances + \
                         (Node, Edge)

    @staticmethod
    def inverse_dict(dicti, value):
        try:
            keys = list(dicti.keys())
            values = list(dicti.values())
            index = values.index(value)
            return keys[index]
        except Exception as e:
            return None

    @classmethod
    def rest_endpoint_to_label(cls, endpoint):
        # TODO the last might not be the most relevant
        endpoint_without_args = endpoint.split("?")[0]
        last_elm = endpoint_without_args.split("/")[-1]
        return StringUtils.standardize_string(last_elm)

    @staticmethod
    def dict_contains_only_attr(data):
        # if its not a dict, then its not an
        # attribute
        if not isinstance(data, dict):
            return False

        data = data.copy()
        if len(data) == 0:
            return False
        attr_names = ["value", "unit"]
        attrs = [data.pop(name, None) for name in attr_names]

        return len(data) == 0

        # def compare_rel(
        #     x): return x.from_edge in item.from_edge.all()

        # def func(x): return any(filter(compare_rel, x.from_edge.all()))
        # any([func(x) for x in same_labels])

        # else:

    @classmethod
    def do_instance_exists(cls, instance):
        search_args = {"pk": instance.pk}
        return cls.find_item(instance, search_args)

    @classmethod
    def do_meta_item_exists(cls, item, parrent_label=None):

        item.label = StringUtils.standardize_string(item.label)
        search_args = cls.build_search_args_for_meta_items(item, parrent_label)
        return cls.find_item(item, search_args)

    @staticmethod
    def find_item(item, search_args):
        item_type = type(item)
        try:
            # this "with transaction.atomic():"
            # is used to make tests run due to some
            # random error, atomic something.
            # it works fine when runs normally

            with transaction.atomic():
                return item_type.objects.get(**search_args)

        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            if hasattr(item, "schema"):
                schema_label = item.schema.label
            else:
                schema_label = item.object.schema.label
            logger.warning("""MultipleObjectsReturned Error, this is most likely wrong wrong, the object
                found:  %s  objects, but the first was chosen.
                -- label: %s schema: %s""" % (
                item_type.objects.filter(**search_args).count(),
                item.label,
                schema_label,
            ))
            return item_type.objects.filter(**search_args).first()
        except Exception as e:
            logger.error(e)

    def _try_create_meta_item(self, item, update=False, parrent_label=None):

        item_type = type(item)
        remove_version = not isinstance(item_type, Schema)

        # test if exists
        item.label = StringUtils.standardize_string(
            item.label, remove_version=remove_version)
        try:
            # this "with transaction.atomic():"
            # is used to make tests run due to some
            # random error, atomic something.
            # it works fine when runs normally
            with transaction.atomic():

                # we want to be able to tell uniquely if this is the same
                # object, so test on all objects, not only the label,
                # so that it is possible to know if we are overwriting
                # objects that shouldnt
                return_item = self.do_meta_item_exists(
                    item, parrent_label=parrent_label)

                # the object exists,
                if return_item:
                    if update or self.overwrite_db_objects:
                        if self.save_to_db:
                            return_item.delete()
                            item.save()

                        else:
                            # if not updated, return the fetched one
                            item = return_item
                    else:
                        item = return_item
                # does not exists, create it!
                else:
                    try:
                        if self.save_to_db:
                            item.save()
                            self.added_meta_items.append(item)

                    except Exception as e:
                        # on update add to debug list
                        self._error_list.append((item, e))
                        return None

            # on success return the item, either fetched, or saved
            # so that the referenced object lives in the database
            self.touched_meta_items.append(item)
            return item

        except (transaction.TransactionManagementError,) as e:
            return None
        except Exception as e:
            return None

    def is_objects_connected(self, obj_from, obj_to, objects):
        relations = obj_from.from_edge.all()

        related_objects = list(map(lambda x: x.to_object.get(), relations))

        related_objects = list(filter(lambda x: x in objects, related_objects))

        for obj in related_objects:
            if obj == obj_to:
                return True
            elif self.is_objects_connected(obj, obj_to, objects):
                return True

        return False

    @staticmethod
    def get_foaf_person():
        schema = Schema.objects.get(label="friend_of_a_friend")
        return SchemaNode.objects.get(label="person", schema=schema)

    @classmethod
    def att_to_att_inst(cls, attr):
        data_type = cls.inverse_dict(SchemaAttribute.data_type_map, attr.data_type)

        return cls.inverse_dict(cls.att_inst_to_type_map, data_type)

    @classmethod
    def get_connected_attribute_pairs(cls, att_1, att_2):

        foaf1, att1_list = BaseMetaDataService.path_to_object(
            att_1, cls.get_foaf_person(), childrens=[])

        foaf2, att2_list = BaseMetaDataService.path_to_object(
            att_2, cls.get_foaf_person(), childrens=[])

        # get first common object
        common_set = set(att1_list) & set(att2_list)
        common_obj = next(filter(lambda x: x in common_set, att1_list))

        # truncate list down to common object
        att1_list = att1_list[:att1_list.index(common_obj) + 1]
        att2_list = att2_list[:att2_list.index(common_obj) + 1]

        returns = []

        common_instances = Node.objects.filter(base=common_obj)
        for common_instance in common_instances:
            value1 = cls.get_specific_child(
                common_instance, att_1, path=att1_list)
            value2 = cls.get_specific_child(
                common_instance, att_2, path=att2_list)
            returns.append((value1, value2))

        return returns

    @classmethod
    def get_specific_child(cls, obj_inst, child, path=None):
        """
        get a decendent object, either att, or obj of a specific type
        """
        if path is None:
            path = cls.path_to_object(child, obj_inst.base)

        search_args = cls.build_search_args_from_list(path, obj_inst)
        AttributeInstance = cls.att_to_att_inst(child)
        try:
            return AttributeInstance.objects.get(**search_args)
        except ObjectDoesNotExist as e:
            return None
        except MultipleObjectsReturned as e:
            print("WARNING: obj, contains multiple object, first is taken")
            return next(AttributeInstance.objects.filter(**search_args))

    @staticmethod
    def build_search_args_from_list(path, obj_inst):
        search_args = {}
        base_arg_name = "from_edge__from_object__"
        arg_name = ""
        # loop though all but last
        for obj in path:
            if isinstance(obj, SchemaAttribute):
                arg_name += "object__"
                search_args["base__label"] = obj.label
            elif obj == obj_inst.base:
                # last elm add primary key
                search_args[arg_name + "pk"] = obj_inst.pk
            else:
                # Not neccesary as long as pk is being added
                # search_args[arg_name + "base__label"] = obj.label
                arg_name += base_arg_name

        return search_args

    @staticmethod
    def path_to_object(obj, root_obj, childrens=()):
        if isinstance(obj, SchemaAttribute):
            # add to path
            childrens.append(obj)
            obj = obj.object
        if obj == root_obj:
            return obj, childrens
        else:
            parrent_rels = obj.from_edge.all()
            childrens.append(obj)
            for parrent_rel in parrent_rels:
                parrent_obj = parrent_rel.from_object

                obj, childrens = BaseMetaDataService.path_to_object(
                    parrent_obj, root_obj, childrens=childrens)

                if obj == root_obj:
                    return obj, list(childrens)

            # this branch has been exhausted, return none
            return None, childrens

    @staticmethod
    def build_search_args_for_meta_items(item, parrent_label):
        search_args = {"label": item.label}

        if isinstance(item, SchemaAttribute):
            search_args["object__label"] = item.object.label

        elif isinstance(item, SchemaNode):
            search_args["schema"] = item.schema
            # adds the option to search for objects dependent
            # on from relations
            if parrent_label and parrent_label == "None":
                search_args["from_edge"] = None
            elif parrent_label:
                search_args["from_edge__from_object__label"] \
                    = parrent_label

        elif isinstance(item, SchemaEdge):
            search_args["from_object"] = item.from_object
            search_args["to_object"] = item.to_object

        return search_args

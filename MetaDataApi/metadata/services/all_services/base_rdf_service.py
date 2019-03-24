from datetime import datetime

from inflection import camelize
from rdflib import Namespace, URIRef
from rdflib.namespace import RDFS, XSD

from MetaDataApi.metadata.models import (
    Object, Attribute, ObjectRelation)
from MetaDataApi.metadata.models import (
    ObjectInstance, ObjectRelationInstance,
    StringAttributeInstance
)
from .base_functions import BaseMetaDataService


class BaseRdfSchemaService(BaseMetaDataService):
    def __init__(self):
        super(BaseRdfSchemaService, self).__init__()

        self.schema = None

        self.default_list = [
            # # 'http://www.w3.org/XML/1998/namespace',
            # "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            # "http://www.w3.org/2000/01/rdf-schema#",
            # "http://purl.org/dc/elements/1.1/",
            # # "http://xmlns.com/wot/0.1/",
            # # "http://www.w3.org/2001/XMLSchema#",
            # "http://www.w3.org/2003/06/sw-vocab-status/ns#",
            # "http://www.w3.org/2002/07/owl#",
            "http://xmlns.com/foaf/0.1/"
        ]
        self.selfhosted = {
            "http://xmlns.com/foaf/0.1/":
            "https://raw.githubusercontent.com/Grusinator/MetaDataApi/" +
                "master/schemas/rdf/imported/foaf.ttl"
        }

        self.rdfs_data_type_map = {
            XSD.dateTime: datetime,
            XSD.float: float,
            XSD.int: int,
            XSD.boolean: bool,
            XSD.string: str,
            RDFS.Literal: str,
        }

        self.valid_data_types = list(self.rdfs_data_type_map.keys())

    def create_uri_ref(self, item):
        # this is just for labeling with letter in uri
        conv = {
            Attribute: "A",
            Object: "O",
            ObjectRelation: "R",

            # instances
            ObjectInstance: "Oi",
            ObjectRelationInstance: "Ri",
            StringAttributeInstance: "Ai",
        }
        # add all types of attr instances
        for item_type in list(self.att_inst_to_type_map.keys()):
            conv[item_type] = "Ai"

        # this is to know where to find the schema
        # it might differ from the schema in the class instance
        schema = item.schema if hasattr(item, "schema") else \
            item.base.schema if hasattr(item, "base") else \
            item.object.schema

        ontology = self.schema_namespace()

        label = item.label if hasattr(item, "label") else \
            item.base.label
        # make sure that there is no space in the url
        label = camelize(label.replace(" ", "_"))

        # if it does not belong to the current schema
        # dont create the
        if self.schema.url != schema.url:
            return URIRef(ontology[label])

        # the first letter is to avoid naming conflict with other
        # objects
        return URIRef(ontology["%s-%s_%s" % (
            conv[type(item)],
            item.pk,
            label)
        ])

    def schema_namespace(self):
        namespace = self.schema.url.replace(".ttl", "")
        namespace += "#"

        # create the corresponding ontology
        return Namespace(namespace)

    def att_instance_to_rdf_type(self, instance):

        inst_type = type(instance)
        dtype = self.att_inst_to_type_map.get(inst_type)

        # inverse of data_type_map
        return self.inverse_dict(self.rdfs_data_type_map, dtype)

    def rdfs_to_att_type(self, type_name):
        # self._split_rdfs_url(range)[1]
        try:
            dtype = self.rdfs_data_type_map.get(type_name)
            return Attribute.data_type_map[dtype]
        except Exception as e:
            return Attribute.data_type_map.get(None)

    def att_type_to_rdfs_uri(self, attr_type):

        # inverse of data_type_map
        data_type = self.inverse_dict(Attribute.data_type_map, attr_type)

        # default to string if nonetype
        data_type = data_type if data_type != type(None) else str
        # inverse self.rdfs_data_type_map lookup
        return self.inverse_dict(self.rdfs_data_type_map, data_type)

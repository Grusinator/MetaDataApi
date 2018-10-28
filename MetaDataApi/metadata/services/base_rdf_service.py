from urllib.error import URLError

from graphql.error import GraphQLLocatedError

import os

from rdflib import Namespace, Graph, Literal, URIRef
from rdflib.namespace import RDF, FOAF, RDFS, DCTERMS, DC, OWL, XSD
from rdflib.plugin import register, Serializer, Parser

from inflection import camelize

from django.core.files.base import ContentFile

from MetaDataApi.datapoints.models import (
    ObjectInstance, ObjectRelationInstance,
    GenericAttributeInstance, StringAttributeInstance,
    DateTimeAttributeInstance, BoolAttributeInstance,
    FloatAttributeInstance, IntAttributeInstance
)
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

from .base_functions import BaseMetaDataService

import uuid
from datetime import datetime


class BaseRdfSchemaService(BaseMetaDataService):
    def __init__(self):
        super(BaseRdfSchemaService, self).__init__()

        self.schema = None

        self.default_list = [
            # 'http://www.w3.org/XML/1998/namespace',
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "http://www.w3.org/2000/01/rdf-schema#",
            "http://purl.org/dc/elements/1.1/",
            # "http://xmlns.com/wot/0.1/",
            # "http://www.w3.org/2001/XMLSchema#",
            "http://www.w3.org/2003/06/sw-vocab-status/ns#",
            "http://www.w3.org/2002/07/owl#",
            "http://xmlns.com/foaf/0.1/"
        ]
        self.selfhosted = {
            "http://xmlns.com/foaf/0.1/":
            "https://raw.githubusercontent.com/Grusinator/MetaDataApi/" +
                "master/schemas/rdf/imported/foaf.ttl"
        }

        self.rdfs_data_type_map = {
            XSD.datetime: datetime,
            XSD.float: float,
            XSD.int: int,
            XSD.bool: bool,
            XSD.string: str,
            RDFS.Literal: str,
        }

        self.valid_datatypes = list(self.rdfs_data_type_map.keys())

    def create_uri_ref(self, item):
        # this is just for labeling with letter in uri
        conv = {
            Attribute: "A",
            Object: "O",
            ObjectRelation: "R",

            # instances
            ObjectInstance: "Oi",
            ObjectRelationInstance: "Ri",
            GenericAttributeInstance: "Ai",
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
            dtype = self.rdfs_type_map.get(type_name)
            return Attribute.data_type_map[dtype]
        except:
            return Attribute.data_type_map.get(None)

    def att_type_to_rdfs_uri(self, attr_type):

        # inverse of data_type_map
        dtype = self.inverse_dict(Attribute.data_type_map, attr_type)

        # default to string if none
        dtype = dtype or str
        # inverse self.rdfs_data_type_map lookup
        return self.inverse_dict(self.rdfs_data_type_map, dtype)

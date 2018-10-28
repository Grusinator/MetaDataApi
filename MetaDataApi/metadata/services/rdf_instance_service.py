from urllib.error import URLError

from graphql.error import GraphQLLocatedError

import os

from rdflib import Namespace, Graph, Literal, URIRef, BNode
from rdflib.namespace import RDF, FOAF, RDFS, DCTERMS, DC, OWL, XSD
from rdflib.plugin import register, Serializer, Parser

from inflection import camelize

from django.core.files.base import ContentFile

from MetaDataApi.datapoints.models import (
    ObjectInstance, ObjectRelationInstance,
    GenericAttributeInstance, StringAttributeInstance,
    DateTimeAttributeInstance, BoolAttributeInstance,
    FloatAttributeInstance, IntAttributeInstance,
    RDFDataDump
)
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation, UnmappedObject)

from .base_functions import BaseMetaDataService

import uuid
from datetime import datetime
from .base_rdf_service import BaseRdfSchemaService


class RdfInstanceService(BaseRdfSchemaService):
    def __init__(self):
        super(RdfInstanceService, self).__init__()

    def export_instances_to_rdf_file(self, schema_label, instance_list):

        # remove unmapped objects
        instance_list = filter(lambda x: not isinstance(
            x, UnmappedObject), instance_list)

        rdf_data = self.export_instances_from_list(schema_label, instance_list)

        content = ContentFile(rdf_data)

        data_dump = RDFDataDump(
            schema=self.schema
        )
        # data_dump.save()
        data_dump.rdf_file.save("%s-%s.ttl" %
                                (schema_label, uuid.uuid4()), content)

        return data_dump.rdf_file

    def export_instances_from_list(self, schema_label, inst_list):
        g = Graph()

        self.schema = Schema.objects.get(label=schema_label)

        # namespace
        g.bind(schema_label, self.schema_namespace())

        for inst in inst_list:
            inst_class_uri = self.create_uri_ref(inst.base)
            # generate a id for the node

            # object
            if isinstance(inst, ObjectInstance):
                # inst name is tag + primary key
                inst_uri = self.create_uri_ref(inst)
                g.add((inst_uri, RDF.type, inst_class_uri))

            # its a attribute type instance
            elif isinstance(inst, tuple(self.att_inst_to_type_map.keys())):
                obj_inst_uri = self.create_uri_ref(inst.object)
                attr_base_uri = self.create_uri_ref(inst.base)

                # TODO is it poosible to specify a more specific datatype
                # rdf_type = self.att_instance_to_rdf_type(inst)

                value = Literal(inst.value)
                g.add((obj_inst_uri, attr_base_uri, value))

            elif isinstance(inst, ObjectRelationInstance):
                from_obj_inst_uri = self.create_uri_ref(inst.from_object)
                to_obj_inst_uri = self.create_uri_ref(inst.to_object)
                relation_base_uri = self.create_uri_ref(inst.base)

                g.add((from_obj_inst_uri, relation_base_uri, to_obj_inst_uri))

        rdf_data = g.serialize(format='turtle')

        return rdf_data

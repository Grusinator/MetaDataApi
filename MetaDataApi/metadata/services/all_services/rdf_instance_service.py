import uuid

from django.core.files.base import ContentFile
from rdflib import Graph, Literal
from rdflib.namespace import RDF

from MetaDataApi.metadata.models import (
    Node, Edge,
    RDFDataDump
)
from MetaDataApi.metadata.models import (
    UnmappedObject)
from .base_rdf_service import BaseRdfSchemaService


class RdfInstanceService(BaseRdfSchemaService):
    def __init__(self):
        super(RdfInstanceService, self).__init__()

    def export_instances_to_rdf_file(self, schema, instance_list):

        # remove unmapped objects
        instance_list = list(filter(lambda x: not isinstance(
            x, UnmappedObject), instance_list))

        rdf_data = self.export_instances_from_list(schema, instance_list)

        content = ContentFile(rdf_data)

        data_dump = RDFDataDump(
            schema=self.schema
        )
        # data_dump.save()
        data_dump.rdf_file.save("%s-%s.ttl" %
                                (schema.label, uuid.uuid4()), content)

        return data_dump.rdf_file

    def export_instances_from_list(self, schema, inst_list):
        g = Graph()

        self.schema = schema

        # namespace
        g.bind(self.schema.label, self.schema_namespace())

        for inst in inst_list:
            inst_class_uri = self.create_uri_ref(inst.base)
            # generate a id for the node

            # object
            if isinstance(inst, Node):
                # inst name is tag + primary key
                inst_uri = self.create_uri_ref(inst)
                g.add((inst_uri, RDF.type, inst_class_uri))

            # its a attribute type instance
            elif isinstance(inst, tuple(self.att_inst_to_type_map.keys())):
                obj_inst_uri = self.create_uri_ref(inst.object)
                attr_base_uri = self.create_uri_ref(inst.base)

                # TODO is it poosible to specify a more specific data_type
                # rdf_type = self.att_instance_to_rdf_type(inst)

                value = Literal(inst.value)
                g.add((obj_inst_uri, attr_base_uri, value))

            elif isinstance(inst, Edge):
                from_obj_inst_uri = self.create_uri_ref(inst.from_object)
                to_obj_inst_uri = self.create_uri_ref(inst.to_object)
                relation_base_uri = self.create_uri_ref(inst.base)

                g.add((from_obj_inst_uri, relation_base_uri, to_obj_inst_uri))

        rdf_data = g.serialize(format='turtle')

        return rdf_data

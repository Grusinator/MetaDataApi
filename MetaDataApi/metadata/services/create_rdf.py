import os
from rdflib import Graph, Literal, URIRef
from rdflib import Namespace
from rdflib.namespace import RDF, FOAF, RDFS, DCTERMS, DC, OWL
from inflection import camelize

from django.core.files.base import ContentFile

from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)


def create_rdf(schema_label):
    g = Graph()

    schema = Schema.objects.get(label=schema_label)

    objects = Object.objects.filter(schema=schema)

    namespace = schema.url.replace(".ttl", "#")

    Ontology = Namespace(namespace)
    g.bind(schema_label, Ontology)

    rdf_schema = URIRef(Ontology)

    # define the ontology
    g.add((rdf_schema, RDF.type, OWL.Ontology))
    g.add((rdf_schema, DC.title, Literal(schema.label)))
    g.add((rdf_schema, DC.description, Literal(schema.description)))

    for object in objects:
        # make sure that there is no space in the url
        obj_label_std = camelize(object.label.replace(" ", "_"))
        obj_name = URIRef(Ontology[obj_label_std])

        # type
        g.add((obj_name, RDF.type, RDFS.Class))
        # description
        g.add((obj_name, RDFS.label, Literal(object.label)))
        g.add((obj_name, RDFS.comment, Literal(object.description)))
        # is defined by what schema
        g.add((obj_name, RDFS.isDefinedBy, rdf_schema))

        relations = ObjectRelation.objects.filter(from_object=object)

        for relation in relations:
            to_obj_label_std = camelize(
                relation.to_object.label.replace(" ", "_"))
            to_object_name = URIRef(Ontology[to_obj_label_std])

            # make sure that there is no space in the url
            rel_label_std = camelize(relation.label.replace(" ", "_"))
            if relation.schema.label == schema_label:

                # the "R_" is to avoid naming conflict with classes
                relation_name = URIRef(Ontology["R_" + rel_label_std])

            else:
                # TODO create the ontology that it belongs to
                relation_name = Literal(rel_label_std)

            # here a realtion object is created
            g.add((relation_name, RDF.type, RDF.Property))

            # a relation is a property with the domain of the object
            # and range another object
            # from_object
            g.add((relation_name, RDFS.domain, obj_name))

            # to_object
            g.add((relation_name, RDFS.range, to_object_name))

            # label and description
            g.add((relation_name, RDFS.label, Literal(relation.label)))
            g.add((relation_name, RDFS.comment,
                   Literal(relation.description)))
            # defined by
            g.add((relation_name, RDFS.isDefinedBy, rdf_schema))

        # add attributes
        for attribute in object.attributes.all():

            # make sure that there is no space in the url
            att_label_std = camelize(attribute.label.replace(" ", "_"))

            # the "A_" is to avoid naming conflict with classes
            attribute_name = URIRef(Ontology["A_" + att_label_std])

            g.add((attribute_name, RDF.type, RDF.Property))

            # this one relates the attribute to the object or domain
            g.add((attribute_name, RDFS.domain, obj_name))

            # datatype
            g.add((attribute_name, RDFS.range, RDFS.Literal))

            # label and description
            g.add((attribute_name, RDFS.label, Literal(attribute.label)))
            g.add((attribute_name, RDFS.comment,
                   Literal(attribute.description)))
            # defined by
            g.add((attribute_name, RDFS.isDefinedBy, rdf_schema))

    ttl_data = g.serialize(format='turtle')

    content = ContentFile(ttl_data)
    # schema.rdf_file.delete()
    schema.rdf_file.save(schema_label + ".ttl", content)

    schema.save()

    return schema.rdf_file.url

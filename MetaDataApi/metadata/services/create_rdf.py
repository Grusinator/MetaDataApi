from rdflib import Graph, Literal, URIRef
from rdflib import Namespace
from rdflib.namespace import RDF, FOAF, RDFS, DCTERMS, DC, OWL

from django.core.files.base import ContentFile

from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

baseschemaurl = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas"


def create_rdf(schema_label):
    g = Graph()

    schema = Schema.objects.get(label=schema_label)

    objects = Object.objects.filter(schema=schema)

    namespace = baseschemaurl + "/" + schema_label + "#"

    Ontology = Namespace(namespace)
    g.bind(schema_label, Ontology)

    rdf_schema = URIRef(Ontology[schema_label])

    # define the ontology
    g.add((rdf_schema, RDF.type, OWL.Ontology))
    g.add((rdf_schema, DC.title, Literal(schema.label)))
    g.add((rdf_schema, DC.description, Literal(schema.description)))

    for object in objects:
        obj_name = URIRef(Ontology[object.label])

        # type
        g.add((obj_name, RDF.type, RDFS.Class))
        # description
        g.add((obj_name, RDFS.label, Literal(object.label)))
        g.add((obj_name, RDFS.comment, Literal(object.description)))
        # is defined by what schema
        g.add((obj_name, RDFS.isDefinedBy, rdf_schema))

        relations = ObjectRelation.objects.filter(from_object=object)

        for relation in relations:
            to_object_name = URIRef(Ontology[relation.to_object.label])
            if relation.schema.label == schema_label:
                relation_name = URIRef(Ontology[relation.label])

            else:
                # TODO create the ontology that it belongs to
                relation_name = Literal(relation.label)

            # g.add((obj_name, relation_name, to_object_name))

        # add attributes
        for attribute in object.attributes.all():
            attribute_name = URIRef(Ontology[attribute.label])

            g.add((attribute_name, RDF.type, RDF.Property))

            # this one relates the attribute to the object
            g.add((attribute_name, RDFS.domain, obj_name))

            # label and description
            g.add((attribute_name, RDFS.label, Literal(attribute.label)))
            g.add((attribute_name, RDFS.comment,
                   Literal(attribute.description)))
            # defined by
            g.add((attribute_name, RDFS.isDefinedBy, rdf_schema))

    ttl_data = g.serialize(format='turtle')

    content = ContentFile(ttl_data)
    schema.rdf_file.delete()
    schema.rdf_file.save(schema_label + ".ttl", content)

    schema.save()

    return schema.rdf_file.url

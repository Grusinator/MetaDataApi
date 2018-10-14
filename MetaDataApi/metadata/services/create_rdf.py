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

    for object in objects:
        obj_name = URIRef(Ontology[object.label])

        g.add((obj_name, RDF.type, OWL.Class))
        g.add((obj_name, DC.description, Literal(object.description)))

        relations = ObjectRelation.objects.filter(from_object=object)

        for relation in relations:

            to_object_name = URIRef(Ontology[relation.to_object.label])
            if relation.schema.label == schema_label:
                relation_name = URIRef(Ontology[relation.label])

            else:
                # TODO create the ontology that it belongs to
                relation_name = Literal(relation.label)

            g.add((obj_name, relation_name, to_object_name))

        # add attributes

    ttl_data = g.serialize(format='turtle')

    content = ContentFile(ttl_data)
    schema.rdf_file.save(schema_label + ".ttl", content)
    schema.save()

    return schema.rdf_file.url

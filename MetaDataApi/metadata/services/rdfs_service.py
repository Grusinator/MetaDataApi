import rdflib
from rdflib.namespace import RDF, FOAF, RDFS, DCTERMS, DC, OWL
from MetaDataApi.metadata.models import (
    Schema, Object,
    Attribute, ObjectRelation)
from urllib.error import URLError
from rdflib.plugin import register, Serializer, Parser
from graphql.error import GraphQLLocatedError

import os
from rdflib import Graph, Literal, URIRef
from rdflib import Namespace
from rdflib.namespace import RDF, FOAF, RDFS, DCTERMS, DC, OWL
from inflection import camelize

from django.core.files.base import ContentFile

from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

from .base_functions import BaseMetaDataService


class RdfService(BaseMetaDataService):
    def __init__(self):
        super(RdfService, self).__init__()

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

        self.valid_datatypes = [
            RDFS.Literal,
        ]

    def export_schema_from_db(self, schema_label):
        g = Graph()
        # reset objects created (exported)
        self._objects_created_list = []

        schema = Schema.objects.get(label=schema_label)

        # to know which have been exported
        self._objects_created_list.append(schema)

        objects = Object.objects.filter(schema=schema)

        # to know which have been exported
        self._objects_created_list.extend(objects)

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
            # to know which have been exported
            self._objects_created_list.extend(relations)

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

            attributes = object.attributes.all()
            # to know which have been exported
            self._objects_created_list.extend(attributes)

            # add attributes
            for attribute in attributes:

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
        # schema.rdfs_file.delete()
        schema.rdfs_file.save(schema_label + ".ttl", content)

        schema.save()

        return schema

    def write_to_db_baseschema(self):
        # not very readable, consider to change to [_ for _ in _ ]
        graph_list = list(map(self._create_graph_from_url, self.default_list))

        schema_list = list(map(lambda x: self._create_schema_from_graph(
            *x), zip(graph_list, self.default_list)))

        dummy = list(map(lambda x: self._create_objects_from_graph(
            *x), zip(graph_list)))

        dummy = list(
            map(self._create_object_references_from_graphV2, graph_list))
        dummy = list(map(self._create_attributes_from_graph, graph_list))

    def write_to_db(self, rdf_url, overwrite=False):

        self.overwrite_db_objects = overwrite

        g = self._create_graph_from_url(rdf_url)

        missing_list = self._validate_dependencies(g)

        self.schema = self._create_schema_from_graph(g, rdf_url)

        self._create_objects_from_graph(g)

        self._create_object_references_from_graphV2(g)

        self._create_attributes_from_graph(g)

    def _create_graph_from_url(self, rdf_url):
        g = rdflib.Graph()
        # if not a string, its not an url
        # assume its a file
        if hasattr(rdf_url, 'read') or rdf_url[-4:] in [".ttl", ".xml"]:
            try:
                # default is n3 (ttl) if not xml (ttl is default)
                format = None if ".xml" in rdf_url else "n3"
                g.parse(rdf_url, format=format)
                return g
            except Exception as e:
                raise Exception("could not load specified file as a graph.")

        # cant load from raw github  ttl if format is not set
        format = "n3" if ".ttl" in rdf_url else None
        schema_name = rdf_url

        register(
            # 'text/rdf+n3', Parser,
            'text/plain', Parser,
            'rdflib.plugins.parsers.notation3', 'N3Parser')

        if rdf_url in self.selfhosted:
            rdf_url = self.selfhosted[rdf_url]
        try:
            g.parse(rdf_url, format=format)
        except URLError as e:
            print("could not fetch schema from url: " + rdf_url)
            return None
        return g

    def _validate_dependencies(self, g):

        missing_list = []
        # recursively try to loo
        for format, namespace in g.namespaces():
            namespace = str(namespace)

            if not self._validate_namespace(namespace):
                print("trying to load missing schema from url")
                missing_list.append(namespace)

        return missing_list

    def _create_schema_from_graph(self, g, rdf_url):
        # identify schema attributes

                # some cases where the url is not the same as the uri
        try:
            schema_subject, _, _ = next(
                g.triples((None,  None, OWL.Ontology)))
        except:
            schema_subject = rdflib.term.URIRef(rdf_url)

        label_keys = [
            RDFS.label,
            DC.title,
            DCTERMS.title
        ]

        description_keys = [
            DC.description,
            DCTERMS.description
        ]

        label = "Not available"
        description = "Not available"

        for key in label_keys:
            try:
                rdf_url, _, label = next(
                    g.triples((schema_subject, key, None)))
                break
            except:
                pass

        for key in description_keys:
            try:
                rdf_url, _, description = next(
                    g.triples((schema_subject, key, None)))
                break
            except:
                pass

        # only save if it does not exists
        try:
            self.schema = Schema.objects.get(url=str(rdf_url))
        except Exception as e:
            self.schema = Schema(
                label=self.standardize_string(label, remove_version=True),
                url=str(rdf_url),
                description=str(description)
            )
            self.schema.save()
        return self.schema

    def _create_objects_from_graph(self, g):
        # now create all objects
        for s, p, o in g.triples((None, None, RDFS.Class)):
            _s = str(s)
            _o = str(o)
            _p = str(p)

            # mandatory
            try:
                # Property label
                label = next(g.triples((s,  RDFS.label, None)))[2]
                # Property Class/domain
                schema_url = next(g.triples((s, RDFS.isDefinedBy, None)))[2]
            except Exception as e:
                continue

            # volentary
            try:
                # Property comment
                comment = next(g.triples((s, RDFS.comment, None)))[2]
            except:
                pass
            try:
                self.schema = Schema.objects.get(url=schema_url)
            except Exception as e:
                pass
            else:
                object = self._try_create_item(
                    Object(
                        label=str(label),
                        description=str(comment),
                        schema=self.schema
                    )
                )

    def _create_object_references_from_graphV2(self, g):
        # object references is in fact rather a
        # property with range and domain pointing at
        # 2 objects

        # now create all object references
        for s, p, o in g.triples((None, None, RDF.Property)):

            # similar to property
            try:
                # Property label
                label = next(g.triples((s,  RDFS.label, None)))[2]
                # Property comment
                try:
                    comment = next(g.triples((s, RDFS.comment, None)))[2]
                except:
                    comment = "could not find"

                # Property Class/domain
                domain = next(g.triples((s, RDFS.domain, None)))[2]
                # Property datatype
                o_range = next(g.triples((s, RDFS.range, None)))[2]

                # the purpose of this is just to identify
                # data properties to avoid database lookup
                # if not needed
                if o_range in self.valid_datatypes:
                    pass

                from_schema_url, from_obj_label = self._split_rdfs_url(domain)
                to_schema_url, to_obj_label = self._split_rdfs_url(o_range)

                # get the schema so that we can select the object from the
                # right schema
                liste = Schema.objects.all()

                # get the right url from either current schema or from other in db
                if self.schema.url == from_schema_url:
                    from_schema = self.schema
                else:
                    from_schema = Schema.objects.get(
                        url=from_schema_url)
                if self.schema.url == to_schema_url:
                    to_schema = self.schema
                else:
                    to_schema = Schema.objects.get(
                        url=to_schema_url)

                # TODO: consider the case if 2 objects has the same label?
                from_object = Object.objects.filter(
                    label=from_obj_label, schema=from_schema).first()
                to_object = Object.objects.filter(
                    label=to_obj_label, schema=to_schema).first()

            # if no such 2 objects exists
            except Exception as e:
                continue
            if from_object and to_object:
                object_relation = self._try_create_item(
                    ObjectRelation(
                        from_object=from_object,
                        to_object=to_object,
                        label=label,
                        schema=self.schema,
                        description=comment
                    )
                )

    def _create_attributes_from_graph(self, g):

        for s, p, o in g.triples((None, None, RDF.Property)):
            _s = str(s)
            _o = str(o)
            _p = str(p)

            try:
                # Property label
                label = next(g.triples((s,  RDFS.label, None)))[2]
                # Property comment
                comment = next(g.triples((s, RDFS.comment, None)))[2]
                # Property Class/domain
                domain = next(g.triples((s, RDFS.domain, None)))[2]
                # Property datatype
                range = next(g.triples((s, RDFS.range, None)))[2]

                _, obj_label = self._split_rdfs_url(domain)
                object = Object.objects.filter(label=obj_label).first()
            except Exception as e:
                continue

            if object is None:
                continue

            if range not in self.valid_datatypes:
                continue

            attribute = self._try_create_item(
                Attribute(
                    datatype=self._split_rdfs_url(range)[1],
                    label=label,
                    object=object
                )
            )

    def _validate_namespace(self, namespace):
        try:
            Schema.objects.Get(url=str(namespace))
        except Exception as e:
            print("schema does not exists")
            return False
        return True

    def _split_rdfs_url(self, url):
        if not isinstance(url, (rdflib.term.URIRef, rdflib.URIRef)):
            return None

        methodlist = [
            lambda x: x.split("#"),
            lambda x: ("/".join(x.split("/")[:-1]) + "/", x.split("/")[-1])
        ]

        for method in methodlist:
            try:
                url, label = method(str(url))
                if label == "":
                    continue

                url += "/" if url[-1] != "/" else ""

                return url, label
            except Exception as e:
                pass
        return None

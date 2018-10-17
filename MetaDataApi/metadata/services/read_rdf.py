import rdflib
from rdflib.namespace import RDF, FOAF, RDFS, DCTERMS, DC, OWL
from MetaDataApi.metadata.models import (
    Schema, Object,
    Attribute, ObjectRelation)
from urllib.error import URLError
from rdflib.plugin import register, Serializer, Parser
from graphql.error import GraphQLLocatedError
from .base_functions import standarize_string


class rdfService:
    def __init__(self):
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
            "http://xmlns.com/foaf/0.1/": "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas/rdf/imported/foaf.ttl"
        }

        self.valid_datatypes = [
            RDFS.Literal,
        ]

    def create_default_schemas(self):
        # not very readable, consider to change to [_ for _ in _ ]
        graph_list = list(map(self.create_graph, self.default_list))

        schema_list = list(map(lambda x: self.create_schema_from_graph(
            *x), zip(graph_list, self.default_list)))

        dummy = list(map(lambda x: self.create_objects_from_graph(
            *x), zip(graph_list)))

        dummy = list(
            map(self.create_object_references_from_graphV2, graph_list))
        dummy = list(map(self.create_attributes_from_graph, graph_list))

    def create_graph(self, rdf_url):
        g = rdflib.Graph()
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

    def rdfs_upload(self, rdf_url):

        g = self.create_graph(rdf_url)

        missing_list = self.validate_dependencies(g)

        self.schema = self.create_schema_from_graph(g, rdf_url)

        self.create_objects_from_graph(g)

        self.create_object_references_from_graphV2(g)

        self.create_attributes_from_graph(g)

    def validate_dependencies(self, g):

        missing_list = []
        # recursively try to loo
        for format, namespace in g.namespaces():
            namespace = str(namespace)

            if not self.validate_namespace(namespace):
                print("trying to load missing schema from url")
                missing_list.append(namespace)

        return missing_list

    def create_schema_from_graph(self, g, rdf_url):
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
                label=standarize_string(label, remove_version=True),
                url=str(rdf_url),
                description=str(description)
            )
            self.schema.save()
        return self.schema

    def create_objects_from_graph(self, g):
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
                object = Object(
                    label=str(label),
                    description=str(comment),
                    schema=self.schema
                )
                object.save()

    def create_object_references_from_graph(self, g):

        def find_object2(g, subject):
            try:
                # Property label
                label = next(g.triples((subject,  RDFS.label, None)))[2]

                # find to_object
                return Object.objects.filter(
                    label=str(label)).first()
            except Exception as e:
                return None
        # now create all object references
        for s, p, o in g.triples((None, None, RDFS.Class)):

            # find the from_class in object table
            from_object = find_object2(g, s)
            if not from_object:
                continue

            for s_s, p_s, o_s in g.triples((s, None, None)):

                # must be URI otherwise it cant be a class
                if not isinstance(o_s, rdflib.term.URIRef):
                    continue

                to_object = find_object2(g, o_s)
                if not to_object:
                    continue

                # create relation
                url, label = self.split_rdfs_url(p_s)

                object_relation = ObjectRelation(
                    from_object=from_object,
                    to_object=to_object,
                    label=label,
                    schema=self.schema
                )
                object_relation.save()

    def create_object_references_from_graphV2(self, g):
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
                comment = next(g.triples((s, RDFS.comment, None)))[2]
                # Property Class/domain
                domain = next(g.triples((s, RDFS.domain, None)))[2]
                # Property datatype
                o_range = next(g.triples((s, RDFS.range, None)))[2]

                if o_range in self.valid_datatypes:
                    pass

                from_schema_url, from_obj_label = self.split_rdfs_url(domain)
                to_schema_url, to_obj_label = self.split_rdfs_url(o_range)

                # get the schema so that we can select the object from the
                # right schema
                liste = Schema.objects.all()

                # get the right url from either current schema or from other in db
                if self.schema.url == from_schema_url:
                    from_schema = self.schema.url
                else:
                    from_schema = Schema.objects.get(
                        url=from_schema_url)
                if self.schema.url == to_schema_url:
                    to_schema = self.schema.url
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
                object_relation = ObjectRelation(
                    from_object=from_object,
                    to_object=to_object,
                    label=label,
                    schema=self.schema,
                    description=comment
                )
                object_relation.save()

    def create_attributes_from_graph(self, g):

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

                _, obj_label = self.split_rdfs_url(domain)
                object = Object.objects.filter(label=obj_label).first()
            except Exception as e:
                continue

            if object is None:
                continue

            if range not in valid_datatypes:
                continue

            attribute = Attribute(
                datatype=self.split_rdfs_url(range)[1],
                label=label,
                object=object
            )
            attribute.save()

    def validate_namespace(self, namespace):
        try:
            Schema.objects.Get(url=str(namespace))
        except Exception as e:
            print("schema does not exists")
            return False
        return True

    def rdfs_download(self, schema=None):
        return

    def split_rdfs_url(self, url):
        if not isinstance(url, (rdflib.term.URIRef, rdflib.URIRef)):
            return None

        methodlist = [
            lambda x: x.split("#"), ,
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

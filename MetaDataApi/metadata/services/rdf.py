import rdflib
from rdflib.namespace import RDF, FOAF, RDFS, DCTERMS, DC, OWL
from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation
from urllib.error import URLError
from rdflib.plugin import register, Serializer, Parser


class rdfService:
    default_list = [
        # 'http://www.w3.org/XML/1998/namespace',
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "http://www.w3.org/2000/01/rdf-schema#",
        "http://purl.org/dc/elements/1.1/",
        # "http://xmlns.com/wot/0.1/",
        # "http://www.w3.org/2001/XMLSchema#",
        "http://www.w3.org/2003/06/sw-vocab-status/ns#",
        "http://www.w3.org/2002/07/owl#"
    ]
    selfhosted = {
        "http://xmlns.com/foaf/0.1/": "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas/foaf.ttl"
    }

    def __init__(self):
        self.schema = None

    def create_default_schemas(self):

        graph_list = list(map(self.create_graph, self.default_list))

        schema_list = list(map(lambda x: self.create_schema_from_graph(
            *x), zip(graph_list, self.default_list)))

        dummy = list(map(lambda x: self.create_objects_from_graph(
            *x), zip(graph_list, schema_list)))

        dummy = list(map(self.create_object_references_from_graph, graph_list))
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

            #            #make sure we are comparing with the right one, else convert to self hosted
            # namespace = self.selfhosted[namespace] if namespace in self.selfhosted else namespace

            # if namespace in self.ignorelist or not force: continue
            # if namespace == schema_name: continue
        try:
            g.parse(rdf_url, format=format)
        except URLError as e:
            return None
        return g

    def rdfs_upload(self, rdf_url):

        g = self.create_graph(rdf_url)

        missing_list = self.validate_dependencies(g)

        schema = self.create_schema_from_graph(g, rdf_url)

        self.create_objects_from_graph(g, schema)

        self.create_object_references_from_graph(g)

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
        schema_subject = rdflib.term.URIRef(rdf_url)
        label_predicate = rdflib.term.URIRef(
            'http://www.w3.org/2000/01/rdf-schema#label')
        description_predicate = rdflib.term.URIRef(
            'http://purl.org/dc/elements/1.1/description')

        try:
            url, _, label = next(
                g.triples((schema_subject,  RDFS.label, None)))
        except:
            try:
                url, _, label = next(
                    g.triples((schema_subject,  DC.title, None)))
            except:
                url = schema_subject
                label = "Not found"
        try:
            url, _, description = next(
                g.triples((schema_subject,  description_predicate, None)))
        except:
            description = "Not available"

        schema = Schema(
            label=str(label),
            url=str(url),
            description=str(description)
        )
        # only save if it does not exists
        # a = Schema.objects.all()
        # if(a != 0):
        schema.save()

        return schema

    def create_objects_from_graph(self, g, schema):
        # now create all objects
        object_list = []
        for s, p, o in g.triples((None,  RDFS.label, None)):
            _s = str(s)
            _o = str(o)
            _p = str(p)

            url, label = self.split_rdfs_url(s)

            # check if no object with that label is created
            if not any(x.label == label for x in object_list):

                # now get description of current subject
                _, _, comment = next(g.triples((s, RDFS.comment, None)))

                label = str(o)

                object = Object(
                    label=label,
                    description=str(comment),
                    schema=schema
                )
                object.save()
                object_list.append(object)

        return 0

    def create_object_references_from_graph(self, g):
        # now create all object references
        def find_object(obj_in, object_list=[]):
            try:
                url, label = self.split_rdfs_url(obj_in)
                return next(filter(lambda x: x.label == label, object_list))
            except:
                try:
                    return Object.objects.filter(label=label).first()
                except Exception as e:
                    return None

        obj_relation_list = []
        for s, p, o in g:
            _s = str(s)
            _o = str(o)
            _p = str(p)

            if not all(isinstance(x, rdflib.term.URIRef) for x in (s, o)):
                continue

            # to be a reference both subject and object must be a object
            # either in this list or in the database
            to_obj = find_object(s)
            from_obj = find_object(o)

            if all((to_obj, from_obj)):
                # get the predicate and split ino label and url
                url, label = self.split_rdfs_url(s)

                object_relation = ObjectRelation(
                    from_object=from_obj,
                    to_object=to_obj,
                    label=label,
                    url=url
                )
                object_relation.save()
                obj_relation_list.append(object_relation)

    def create_attributes_from_graph(self, g):
        attribute_list = []
        for s, p, o in g.triples((None, None, None)):
            _s = str(s)
            _o = str(o)
            _p = str(p)

            if not all((
                    isinstance(s, rdflib.term.URIRef),
                    not isinstance(o, rdflib.term.URIRef))):
                continue

            try:
                obj_label = str(s).split("#")[1]
                object = Object.objects.filter(label=obj_label).first()
            except Exception as e:
                pass
            finally:
                # get the predicate and split ino label and url
                _, label = str(p).split("#")

                datatype = str(type(o))

                attribute = Attribute(
                    datatype=datatype,
                    label=label,
                    object=object
                )
                attribute.save()
                attribute_list.append(attribute)

            # literals = list(map(lambda x: x if isinstance(x, rdflib.term.URIRef) else None, (s,p,o)))
            # if any(l is not None for l in literals):
            #    literals

            # _s = str(s)
            # _o = str(o)
            # _p = str(p)

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
            lambda x: x.split("#"),
            lambda x: ("/".join(x.split("/")[:-1]), x.split("/")[-1])
        ]

        for method in methodlist:
            try:
                url, label = method(str(url))
                if label == "":
                    continue
                return url, label
            except Exception as e:
                pass
        return None

import rdflib
from rdflib.namespace import RDF, FOAF, RDFS, DCTERMS, OWL
from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation

class rdfService:
    ignorelist = [
        'http://www.w3.org/XML/1998/namespace',
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "http://www.w3.org/2000/01/rdf-schema#",
        "http://purl.org/dc/elements/1.1/",
        "http://xmlns.com/wot/0.1/",
        "http://www.w3.org/2001/XMLSchema#",
        "http://www.w3.org/2003/06/sw-vocab-status/ns#",
        "http://www.w3.org/2002/07/owl#"
        ]
    selfhosted = {
            "http://xmlns.com/foaf/0.1/": "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas/foaf.ttl"
        }

    def __init__(self):
        self.schema = None


    def rdfs_upload(self, rdf_data, force=False):
        g=rdflib.Graph()
        rdf_data = self.selfhosted[rdf_data] if rdf_data in self.selfhosted else rdf_data
        
        #cant load from raw github  ttl if format is not set 
        format = "n3" if ".ttl" in rdf_data else None

        g.parse(rdf_data, format=format)

        missing_list = self.validate_dependencies(g)

        self.create_schema_from_graph(g)

        self.create_objects_from_graph(g)

        self.create_object_references_from_graph(g)



    def validate_dependencies(self, g):

        missing_list = [] 
        #recursively try to loo
        for format, namespace in g.namespaces():
            namespace = str(namespace)

            #make sure we are comparing with the right one, else convert to self hosted
            namespace = self.selfhosted[namespace] if namespace in self.selfhosted else namespace
        
            if namespace in self.ignorelist or not force: continue
            if namespace == rdf_data: continue
            
            if not self.validate_namespace(namespace):
                print("trying to load missing schema from url")
                missing_list.append(namespace)
        
        return missing_list

    def create_schema_from_graph(self, g):
        #identify schema attributes
        schema_subject = rdflib.term.URIRef(rdf_data)
        label_predicate = rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#label')
        description_predicate = rdflib.term.URIRef('http://purl.org/dc/elements/1.1/description')

        url,_,label = next(g.triples( (schema_subject,  label_predicate, None)))
        url,_,description = next(g.triples( (schema_subject,  description_predicate, None)))

        schema = Schema(
           label = str(label),
           url = str(url),
           description = str(description)
        )
        schema.save()

    def create_objects_from_graph(self, g):
        #now create all objects 
        object_list = []
        for s,p,o in g.triples( (None,  RDFS.label, None)):
            _s = str(s)
            _o = str(o)
            _p = str(p)
            try:
                label = str(s).split("#")[1]
                if label == "": continue
            except:
                #there must be a # to identify that it is a class
                #otherwise we might get the label of something else
                continue

            #check if no object with that label is created
            if not any(x.label == label for x in object_list):

                #now get description of current subject
                _,_,comment = next(g.triples( (s, RDFS.comment, None)))

                object_list.append(
                    Object(
                        label = label,
                        description = str(comment),
                        schema = schema
                    )
                )

        map(lambda x: x.save(), object_list)

    def create_object_references_from_graph(self):
        #now create all object references
        def find_object(obj_in, object_list):
            try:
                label = str(obj_in).split("#")[1]
                return next(filter(lambda x: x.label == label, object_list))
            except:
                try:
                    return Object.objects.get(label=label)
                except:
                    return None
        
        obj_relation_list = []
        for s,p,o in g:
            _s = str(s)
            _o = str(o)
            _p = str(p)
            #to be a reference both subject and object must be a object
            #either in this list or in the database
            to_obj = find_object(s, object_list)
            from_obj = find_object(o, object_list)
            
            if all((to_obj, from_obj)):
                #get the predicate and split ino label and url
                url,label = str(p).split("#")

                obj_relation_list.append(
                    ObjectRelation(
                        from_object=from_obj,
                        to_object=to_obj,
                        label=label,
                        url=url
                    )
                )

        map(lambda x: x.save(), obj_relation_list)
            
            
            
            
            #literals = list(map(lambda x: x if isinstance(x, rdflib.term.URIRef) else None, (s,p,o)))
            #if any(l is not None for l in literals):
            #    literals

            #_s = str(s)
            #_o = str(o)
            #_p = str(p)

    def validate_namespace(self, namespace):
        try:
            Schema.objects.Get(url=str(namespace))
        except:
            print("schema does not exists")
            return False
        return True

    def rdfs_download(self, schema=None):
        return


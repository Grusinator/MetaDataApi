import rdflib
from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation

class rdfService:
    ignorelist = [
        'http://www.w3.org/XML/1998/namespace',
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "http://www.w3.org/2000/01/rdf-schema#"
        ]
    selfhosted = {
            "http://xmlns.com/foaf/0.1/": "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas/foaf.ttl"
        }

    def rdfs_upload(self, rdf_data):
        g=rdflib.Graph()
        
        if rdf_data in self.selfhosted:
            rdf_data = self.selfhosted[rdf_data]
        
        if "http://" in rdf_data or "https://" in rdf_data:
            g.parse(rdf_data)
        else:  
            g.load(rdf_data)

        #recursively try to 
        for format, namespace in g.namespaces():
            namespace = str(namespace)
            if namespace in self.ignorelist: continue
            if namespace == rdf_data: continue
            
            if not self.validate_namespace(namespace):
                print("trying to load missing schema from url")
                self.rdfs_upload(namespace)

        g.label

        for s,p,o in g:
            literals = list(map(lambda x: x if isinstance(x, rdflib.term.URIRef) else None, (s,p,o)))
            if any(l is not None for l in literals):
                literals

            _s = str(s)
            _o = str(o)
            _p = str(p)

    def validate_namespace(self, namespace):
        try:
            Schema.objects.Get(url=str(namespace))
        except:
            print("schema does not exists")
            return False
        return True

    def rdfs_download(self, schema=None):
        return


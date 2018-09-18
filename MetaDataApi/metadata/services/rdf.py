import rdflib
from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation

class rdfService:

    def rdfs_upload(self, rdf_data):
        g=rdflib.Graph()
        g.load(rdf_data)

        g.

        for s,p,o in g:
            literals = list(map(lambda x: x if isinstance(x, rdflib.term.Literal) else None, (s,p,o)))
            if any(l is not None for l in literals):
                literals
            _s = str(s)
            _o = str(o)
            _p = str(p)


    def rdfs_download(self, schema=None):
        return


from inflection import underscore
from gensim.models import word2vec
from MetaDataApi.metadata.models import (
    Schema, Object,
    Attribute, ObjectRelation)


class AttributeIdentification():
    def __init__(self, *args, **kwargs):
        sentences = word2vec.Text8Corpus('text8')

        self.orms = [Object, Attribute, ObjectRelation, Schema]

        self.model = word2vec.Word2Vec(sentences, size=200)

    def find_label_in_metadata(str: label, data_type):
        # iterate through the vectorized  dataobjects,
        # mostly objects and attributes.
        # Add semantic vector to each object

        candidates = []
        # first, test if label exists in each object
        for orm in self.orms:
            objects = orm.objects.filter(label=label)

    def likelihood_score(object, data_type):
        return 0

    def compare_labels(label1, label2):
        label1 = underscore(label1)
        label2 = underscore(label2)

        self.model.similarity(label1, label2)

    def datatype_match(data_type,)


class DataType:

    __init__(self, datatype, mean, std, *args, **kwargs):
        pass

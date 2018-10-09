import json

from inflection import underscore
from gensim.models import word2vec
from MetaDataApi.metadata.models import (
    Schema, Object,
    Attribute, ObjectRelation)


class SchemaIdentification():
    def __init__(self, *args, **kwargs):
        # consider using sports articles for corpus
        # sentences = word2vec.Text8Corpus('text8')

        self.orms = [Object, Attribute, ObjectRelation, Schema]

        # self.model = word2vec.Word2Vec(sentences, size=200)

    def identify_data(self, input_data):
        """ this is the main function that handles all the
        restructuring of the data.
        """

        input_data = json.loads(input_data)

        # for each branch in the tree check match for labels,
        # attribute labels and relations labels
        for key, value in input_data.items():
            # this is likely a object if it contains other
            # attributes or objects
            if isinstance(value, dict):
                # check if the key is a label
                obj = self.find_label_in_metadata(key)
            elif isinstance(value, [str, int, float]):
                # it is probably an attribute
                data_type = self.identify_datatype(value)
                obj = self.find_label_in_metadata(key, data_type)

    def identify_datatype(self, element):
        # even though it is a string,
        # it might really be a int or float
        # so if string verify!!
        if isinstance(element, str):
            try:
                val = float(element)
            except ValueError:
                # its probably a string
                return str

            if element.contains("."):
                return float
            else:
                return int
        else:
            # otherwise just return the type of
            return type(element)

    def find_label_in_metadata(self, label, data_type=None):
        # iterate through the vectorized  dataobjects,
        # mostly objects and attributes.
        # Add semantic vector to each object

        candidates = []
        # first, test if label exists in each object
        for orm in self.orms:
            objects = orm.objects.all()
            for obj in objects:
                score = self.likelihood_score(label, obj, data_type)
                if score > 0.7:
                    candidates.append((obj, score))

    def likelihood_score(self, label, obj, data_type=None):
        v1 = self.compare_labels(label, obj.label)

        # datatype is only used in case of attributes
        if isinstance(obj, Attribute) and data_type:
            v2 = self.datatype_match(obj, data_type)
        # if it is an object we can look at the relations
        # and see if it matches related objects or attributes
        elif isinstance(obj, Object):
            v2 = self.relations_match()
        else:
            v2 = 0
        return v1 + v2

    def compare_labels(self, label1, label2):
        label1 = underscore(label1)
        label2 = underscore(label2)

        # this is a perfect match
        if label1 == label2:
            return 1
        else:
            # probably need more preprocessing
            return self.model.similarity(label1, label2)

    def datatype_match(self, object, data_type):
        return 0

    def relations_match(self, object, json_desendents, json_parrent):
        """
        check if there are similarities with the structure
        """
        return 0


class DataType:

    def __init__(self, datatype, mean, std, *args, **kwargs):
        pass

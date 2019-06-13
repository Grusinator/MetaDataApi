from django.db.models import ForeignKey, OneToOneField
from rest_framework.serializers import ModelSerializer


class SerializableModel:
    model_relations = (ForeignKey, OneToOneField,)

    def build_serializer(self):
        properties = self.build_properties()
        return type(self.__name__ + "Serializer", (ModelSerializer,), properties)

    def build_properties(self) -> dict:
        properties = {"Meta": self.build_meta_class()}
        for relation_name, relation_serializer in self.get_relations().items():
            properties[relation_name] = relation_serializer
        return properties

    def get_relations(self) -> dict:
        pass

    def build_meta_class(self):
        return type(
            "Meta", (),
            {"ignore": ["id"] + self.get_all_model_relations_names()}
        )

    def get_all_model_relations_names(self) -> list:
        class_properties = self.__dict__.items()
        model_relation_properties = filter(lambda x: isinstance(x.value, self.model_relations), class_properties)
        return [k for k, v in model_relation_properties]

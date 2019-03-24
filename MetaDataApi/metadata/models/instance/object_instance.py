from django.db import models

from MetaDataApi.metadata.models.instance.instance_base import BaseInstance
from MetaDataApi.metadata.utils import BuildDjangoSearchArgs
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils


class ObjectInstance(BaseInstance):
    base = models.ForeignKey('Object', on_delete=models.CASCADE)

    def __str__(self):
        return "Oi:%s.%s" % (self.base.schema.label, self.base.label)

    @classmethod
    def exists(cls, label, children={}):
        arg_builder = BuildDjangoSearchArgs()
        search_args = arg_builder.build_from_json(children)
        search_args["label"] = label
        search_args = BuildDjangoSearchArgs.modify_keys_in_dict(
            search_args, lambda x: "base__" + x)

        return DjangoModelUtils.get_object_or_none(cls, **search_args)

    def get_related_list(self, include_attributes=False):
        related = []

        builder = BuildDjangoSearchArgs()

        # add "to" relations to current object to list
        # dont match on label but on object
        builder.add_to_obj(self)

        related.extend(list(type(self).objects.filter(**builder.search_args)))

        # clear args
        builder.search_args = {}

        # add "from" relations to current object to list
        # dont match on label but on object
        builder.add_from_obj(self)
        related.extend(list(type(self).objects.filter(**builder.search_args)))

        if include_attributes:
            raise NotImplementedError(
                "include atts has not been implemented yet")
            # TODO add all types of attributes
            # related.append(Attribute.objects.filter(object=self))

        return related

    # def object_childrens_to_json(self):
    #     raise NotImplementedError

    class Meta:
        app_label = 'metadata'
        default_related_name = '%(model_name)s'

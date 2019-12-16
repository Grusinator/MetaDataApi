from django.core.exceptions import ValidationError
from django.db import models

from MetaDataApi.utils.django_model_utils import DjangoModelUtils
from .BaseInstance import BaseInstance


class Edge(BaseInstance):
    base = models.ForeignKey('SchemaEdge', on_delete=models.CASCADE, related_name="instances")

    from_object = models.ForeignKey('Node', related_name='to_edge', on_delete=models.CASCADE)
    to_object = models.ForeignKey('Node', related_name='from_edge', on_delete=models.CASCADE)

    def __str__(self):
        return "Ri:%s - %s - %s" % (
            self.base.from_object.label,
            self.base.label,
            self.base.to_object.label
        )

    class Meta:
        app_label = 'metadata'
        default_related_name = '%(model_name)s'
        unique_together = ("base", "from_object", "to_object")

    @classmethod
    def exists(cls, base__label: str, from_object__base__label: str,
               to_object__base__label: str):

        search_args = dict(locals())
        search_args.pop("cls")

        return DjangoModelUtils.get_object_or_none(cls, **search_args)

    # custom restrictions on foreign keys to make sure the instances are of
    # the right meta object type
    def save(self, *args, **kwargs):
        if self.from_object.base != self.base.from_object:
            raise ValidationError(
                "from_object instance must match the base from_object")
        if self.to_object.base != self.base.to_object:
            raise ValidationError(
                "to_object instance must match the base to_object")

        return super(Edge, self).save(*args, **kwargs)

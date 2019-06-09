import graphene
from graphene import (ObjectType, Field)
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required

from MetaDataApi.metadata.models import (
    Node,
    FloatAttribute,
    StringAttribute,
    DateTimeAttribute)
from MetaDataApi.metadata.schema.meta_schema import AttributeNode as AttributeMetaNode
from MetaDataApi.metadata.services.services import GetTemporalFloatPairsService
from MetaDataApi.users.schema import UserType


# from MetaDataApi.datapoints.services.sound_processing_services import SoundClassifier

class ObjectInstanceNode(DjangoObjectType):
    class Meta:
        model = Node
        filter_fields = {
            'base__label': ["icontains", "exact", "istartswith"]
        }
        interfaces = (graphene.relay.Node, )


class StringAttributeNode(DjangoObjectType):
    class Meta:
        model = StringAttribute
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            "base__label": ["exact", "icontains", "istartswith"]
        }


class TemporalAttributeNode(DjangoObjectType):
    class Meta:
        model = DateTimeAttribute
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            "base__label": ["exact", "icontains", "istartswith"]
        }


class FloatAttributeNode(DjangoObjectType):
    class Meta:
        model = FloatAttribute
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            "base__label": ["exact", "icontains", "istartswith"]
        }


class TemporalFloatAttributeNode(ObjectType):
    value = Field(FloatAttributeNode)
    datetime = Field(TemporalAttributeNode)


class GenericAttributeNode(ObjectType):
    base = Field(AttributeMetaNode)
    value = graphene.String()
    object = Field(ObjectInstanceNode)
    owner = Field(UserType)

    class Meta:
        interfaces = (graphene.relay.Node, )


# test upload
class GetTemporalFloatPairs(graphene.Mutation):
    data = graphene.List(TemporalFloatAttributeNode)

    class Arguments:
        schema_label = graphene.String()
        object_label = graphene.String()
        attribute_label = graphene.String()
        datetime_label = graphene.String()
        datetime_object_label = graphene.String()

    def mutate(self, info, schema_label, object_label,
               attribute_label, datetime_label=None,
               datetime_object_label=None):

        args = locals()
        [args.pop(x) for x in ["info", "self", "args"]]
        args["user_pk"] = info.context.user.pk

        data = GetTemporalFloatPairsService.execute(args)

        return_data = [TemporalFloatAttributeNode(
            value=value, datetime=datetime)
            for value, datetime in data]

        return GetTemporalFloatPairs(data=return_data)


# test upload
class UploadFile(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # file parameter is key to uploaded file in FILES from context
        uploaded_file = info.context.FILES.get(file)
        # do something with your file

        return UploadFile(success=uploaded_file is not None)


class Upload2Files(graphene.Mutation):
    class Arguments:
        files = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, files, **kwargs):
        # file parameter is key to uploaded file in FILES from context
        uploaded_file = info.context.FILES.get(files[0])
        uploaded_file = info.context.FILES["0"]
        uploaded_file2 = info.context.FILES.get(files[1])
        # do something with your file

        return UploadFile(success=uploaded_file is not None)

# wrap all queries and mutations


class Query(graphene.ObjectType):
    object_instance = graphene.relay.Node.Field(ObjectInstanceNode)
    all_object_instances = DjangoFilterConnectionField(ObjectInstanceNode)

    attribute_instance = graphene.relay.Node.Field(StringAttributeNode)
    all_attribute_instances = DjangoFilterConnectionField(StringAttributeNode)

    float_attribute_instance = graphene.relay.Node.Field(FloatAttributeNode)
    all_float_attribute_instances = DjangoFilterConnectionField(
        FloatAttributeNode)

    all_generic_attribute_instances = graphene.List(
        GenericAttributeNode)

    @login_required
    def resolve_all_generic_attribute_instances(self, info):
        att_instance_types = [DateTimeAttribute,
                              FloatAttribute, StringAttribute]

        generic_list = []
        for AttributeInstance in att_instance_types:
            for att_inst in AttributeInstance.objects.filter(owner=info.context.user):
                gen_att_inst = GenericAttributeNode(
                    value=str(att_inst.value),
                    owner=att_inst.owner,
                    base=att_inst.base,
                    object=att_inst.object
                )
                generic_list.append(gen_att_inst)

        return generic_list


class Mutation(graphene.ObjectType):
    upload_file = UploadFile.Field()
    upload2_files = Upload2Files.Field()
    get_temporal_float_pairs = GetTemporalFloatPairs.Field()

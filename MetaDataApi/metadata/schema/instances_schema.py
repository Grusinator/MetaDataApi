import graphene
from graphene import (ObjectType, Field, Enum)
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql.error import GraphQLError
from graphql_jwt.decorators import login_required

from MetaDataApi.metadata.models import (
    Attribute, Object, Schema
)
from MetaDataApi.metadata.models import (
    RawData, CategoryTypes,
    ObjectInstance,
    FloatAttributeInstance,
    StringAttributeInstance,
    DateTimeAttributeInstance)
from MetaDataApi.metadata.schema.meta_schema import AttributeNode as AttributeMetaNode
from MetaDataApi.metadata.services.services import GetTemporalFloatPairsService
from MetaDataApi.users.schema import UserType
from datapoints.schema_processing import ProcessRawData

# from datapoints.services.sound_processing_services import SoundClassifier

GrapheneCategoryTypes = Enum.from_enum(CategoryTypes)


# specific ( only for query )


class RawDataType(DjangoObjectType):
    class Meta:
        model = RawData
        interfaces = (graphene.relay.Node, )
        filter_fields = ['value', ]


class ObjectInstanceNode(DjangoObjectType):
    class Meta:
        model = ObjectInstance
        filter_fields = {
            'base__label': ["icontains", "exact", "istartswith"]
        }
        interfaces = (graphene.relay.Node, )


class StringAttributeNode(DjangoObjectType):
    class Meta:
        model = StringAttributeInstance
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            "base__label": ["exact", "icontains", "istartswith"]
        }


class TemporalAttributeNode(DjangoObjectType):
    class Meta:
        model = DateTimeAttributeInstance
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            "base__label": ["exact", "icontains", "istartswith"]
        }


class FloatAttributeNode(DjangoObjectType):
    class Meta:
        model = FloatAttributeInstance
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


class CreateRawData(graphene.Mutation):
    rawdata = Field(RawDataType)

    class Arguments:
        starttime = graphene.DateTime()
        stoptime = graphene.DateTime()
        files = Upload()  # image and audio
        value = graphene.Float()
        std = graphene.Float()
        text = graphene.String()

        # meta params
        source = graphene.String()
        category = GrapheneCategoryTypes()
        label = graphene.String()

    @login_required
    def mutate(self, info, source, category, label, starttime, stoptime=None,
               value=None, std=None, text=None, files=None):

        # handle metadata here

        # Raw data should be processed into datapoints
        try:
            function = ProcessRawData.select_mutate_variant(self, category)

            datalist = function(self, info, source, category, label, starttime,
                                stoptime=None, value=None, std=None, text=None,
                                files=None)

            for data in datalist:
                if isinstance(StringAttributeInstance):
                    data.save()
                elif isinstance(RawData):
                    data.metadata = None
                    data.save()
                    # make sure that the raw data is passed to response
                    rawdata = data
        except:
            pass
            print("eror occored while processing raw data..")

            rawdata = RawData(
                starttime=starttime,
                stoptime=stoptime,
                image=None,
                audio=None,
                value=value,
                std=std,
                text=text,
                metadata=None,
                owner=info.context.user
            )

            rawdata.save()

        return CreateRawData(rawdata=rawdata)


class CreateDatapoint(graphene.Mutation):
    datapoint = Field(GenericAttributeNode)
    # TODO create mutations for each data_type using metaclasses

    class Arguments:
        value = graphene.Float()
        meta_attribute = graphene.String()
        meta_object = graphene.String()
        meta_schema = graphene.String()

    @login_required
    def mutate(self, info, meta_schema, meta_object, meta_attribute,
               value):

        raise NotImplementedError()
        # get the object type from metadata and create an instance
        try:
            schema = Schema.objects.get(label=meta_schema)
            object = Object.objects.get(
                label=meta_object,
                schema=schema)
            attribute = Attribute.objects.get(
                label=meta_attribute,
                object=object)
        except Exception as e:
            raise GraphQLError(
                """no metadata object correspond to the
                combination of source, category and label""")

        object_inst = ObjectInstance(
            base=object,
            schema=schema,
            owner=info.context.user
        )

        object_inst.save()

        return CreateDatapoint(datapoint)


class CreateRawData(graphene.Mutation):
    rawdata = Field(RawDataType)

    class Arguments:
        starttime = graphene.DateTime()
        stoptime = graphene.DateTime()
        files = Upload()  # image and audio
        value = graphene.Float()
        std = graphene.Float()
        text = graphene.String()

        # meta params
        source = graphene.String()
        category = GrapheneCategoryTypes()
        label = graphene.String()

    @login_required
    def mutate(self, info, source, category, label, starttime, stoptime=None,
               value=None, std=None, text=None, files=None):

        # handle metadata here

        # Raw data should be processed into datapoints
        try:
            function = ProcessRawData.select_mutate_variant(self, category)

            datalist = function(self, info, source, category, label, starttime,
                                stoptime=None, value=None, std=None, text=None,
                                files=None)

            for data in datalist:
                if isinstance(StringAttributeInstance):
                    data.save()
                elif isinstance(RawData):
                    data.metadata = None
                    data.save()
                    # make sure that the raw data is passed to response
                    rawdata = data
        except:
            pass
            print("eror occored while processing raw data..")

            rawdata = RawData(
                starttime=starttime,
                stoptime=stoptime,
                image=None,
                audio=None,
                value=value,
                std=std,
                text=text,
                metadata=None,
                owner=info.context.user
            )

            rawdata.save()

        return CreateRawData(rawdata=rawdata)


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
    # TODO add attribute querys by using decorator or metaclass
    all_rawdata = graphene.List(RawDataType)

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
        att_instance_types = [DateTimeAttributeInstance,
                              FloatAttributeInstance,  StringAttributeInstance]

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

    @login_required
    def resolve_all_rawdata(self, info):
        datapointlist = RawData.objects.filter(owner=info.context.user)
        return datapointlist


class Mutation(graphene.ObjectType):
    create_datapoint = CreateDatapoint.Field()
    create_rawdata = CreateRawData.Field()
    upload_file = UploadFile.Field()
    upload2_files = Upload2Files.Field()
    get_temporal_float_pairs = GetTemporalFloatPairs.Field()

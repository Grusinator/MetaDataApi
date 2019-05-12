from MetaDataApi.metadata.models import StringAttributeInstance, ObjectInstance, Object, Schema


class InstanceMocks:

    @staticmethod
    def ObjectInstance1():
        schema = Schema.create_new_empty_schema("meta_data_api")
        obj = Object(label="dummy", schema=schema)
        return ObjectInstance(
            base=obj
        )

    @staticmethod
    def MockStringAttributeInstance():
        return StringAttributeInstance(
            value="somevalue",
            obj=InstanceMocks.ObjectInstance1()
        )

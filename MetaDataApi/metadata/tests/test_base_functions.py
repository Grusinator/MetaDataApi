import django
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command
from MetaDataApi.metadata.services.data_cleaning_service import (
    DataCleaningService
)


class TestMetadataBaseFunctionService(TransactionTestCase):
    """Tests for the application views."""
    # fixtures = [
    #     'metadata/fixtures/new_load.json',
    # ]

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestMetadataBaseFunctionService, cls).setUpClass()
        django.setup()

    def test_identify_json_data_sample(self):
        from MetaDataApi.metadata.services.base_functions import (
            BaseMetaDataService)
        from MetaDataApi.metadata.models import (
            Object, Attribute, ObjectRelation, Schema)

        service = BaseMetaDataService()
        schema = service.create_new_empty_schema("test")

        # self
        test_list = [
            Object(
                schema=schema,
                label="obj1"),
            Object(
                schema=schema,
                label="obj2"),
            Object(
                schema=schema,
                label="obj3")
        ]

        test_list.extend(
            [
                Attribute(
                    label="att1",
                    object=test_list[0]
                ),
                Attribute(
                    label="att2",
                    object=test_list[1]
                ),
                ObjectRelation(
                    schema=schema,
                    label="rel1",
                    from_object=test_list[1],
                    to_object=test_list[2]
                ),
                ObjectRelation(
                    schema=schema,
                    label="rel2",
                    from_object=test_list[0],
                    to_object=test_list[2]
                )
            ]
        )

        resp = [service.is_meta_item_in_created_list(
            elm, test_list) is not None for elm in test_list]

        self.assertListEqual(resp, [True] * len(resp))

        # fail
        expected_to_fail = [
            Attribute(
                label="att3",
                object=test_list[1]
            ),
            Attribute(
                label="att2",
                object=test_list[2]
            ),
            Object(
                schema=schema,
                label="obj4")
        ]

        resp = [service.is_meta_item_in_created_list(
            elm, test_list) is not None for elm in expected_to_fail]

        self.assertListEqual(resp, [False] * len(resp))

        # pass
        expected_to_pass = [
            Attribute(
                label="att1",
                object=Object(
                    schema=schema,
                    label="obj1"
                )
            ),
            Attribute(
                label="att2",
                object=test_list[2]
            ),
            Object(
                schema=schema,
                label="obj4")
        ]

        resp = [service.is_meta_item_in_created_list(
            elm, test_list) is not None for elm in expected_to_pass]

        self.assertListEqual(resp, [True] * len(resp))

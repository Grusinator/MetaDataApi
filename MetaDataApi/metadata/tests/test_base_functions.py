import django
from django.test import TransactionTestCase

from MetaDataApi.metadata.tests.data import LoadTestData


class TestMetadataBaseFunctionService(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestMetadataBaseFunctionService, cls).setUpClass()
        django.setup()

    def test_path_to_foaf_person(self):
        from MetaDataApi.metadata.services import BaseMetaDataService
        from MetaDataApi.metadata.models import (
            Object, Attribute)

        LoadTestData.init_foaf()

        att = Attribute(object=Object.objects.get(label="image"),
                        label="test_att",
                        data_type="float")
        att.save()
        service = BaseMetaDataService()
        foaf, to_foaf_p_list = service.path_to_object(
            att, service.get_foaf_person())

        self.assertListEqual(to_foaf_p_list, [att, att.object, ])

    def test_get_connected_pair(self):
        from MetaDataApi.metadata.models import Attribute
        from MetaDataApi.metadata.services import BaseMetaDataService
        LoadTestData.init_strava_schema_from_file()
        LoadTestData.init_strava_data_from_file()
        service = BaseMetaDataService()

        att1 = Attribute.objects.get(
            label="name", object__schema__label="strava")
        att2 = Attribute.objects.get(
            label="distance", object__schema__label="strava")

        data = service.get_connected_attribute_pairs(att1, att2)

        expected = []

        self.assertListEqual(data, expected)

    def test_is_object_in_list(self):
        from MetaDataApi.metadata.services.base_functions import (
            BaseMetaDataService)
        from MetaDataApi.metadata.models import (
            Object, Attribute, ObjectRelation)

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

        # self.assertListEqual(resp, [True] * len(resp))

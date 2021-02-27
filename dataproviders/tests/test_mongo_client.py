from dataproviders.services.pymongo_client import PyMongoClient


class TestMongoClient:
    mongo_client = PyMongoClient()

    def test_connection_to_mongo(self):
        db = self.mongo_client.client.test
        assert db.name == "test"

    def test_insert_data(self, ):
        self.mongo_client.insert_data("test", "endpoint", "william", "010891", {"age": 27})

    def test_get_data(self):
        value = self.mongo_client.get_data("test", "endpoint", "william", "010891")
        assert value[0].get("data").get("age") == 27

import pymongo



class PyMongoClient:
    def __init__(self):
        host = "localhost"
        port = 27017
        username = "django"
        password = "dev1234"
        conn_string = f"mongodb://{username}:{password}@{host}:{port}/?authSource=admin"
        self.client = pymongo.MongoClient(conn_string, 27017)

    def insert_data(self, provider, endpoint_name, user, timestamp, data):
        collection = self.get_collection(provider, endpoint_name)
        data_with_meta = {
            "provider": provider,
            "user": user,
            "time_stamp": timestamp,
            "data": data,
        }
        collection.insert_one(data_with_meta)

        # db.my_collection.create_index("x")

        # for item in db.my_collection.find().sort("x", pymongo.ASCENDING):
        #     print(item["x"])
        #
        # [item["x"] for item in db.my_collection.find().limit(2).skip(1)]

    def get_collection(self, provider, endpoint_name):
        db_name = provider
        db = getattr(self.client, db_name)
        collection_name = f"{provider}_{endpoint_name}"
        collection = getattr(db, collection_name)
        return collection

    def get_data(self, provider, endpoint, user, timestamp, filter=None, sort=None):
        collection = self.get_collection(provider, endpoint)
        return [elm for elm in collection.find()]

import pymongo

from model.account import createAccountModel, updateAccountModel


class MongoDB:
    def __init__(self, host, port, user, password, auth_db, db, collection):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.auth_db = auth_db
        self.db = db
        self.collection = collection
        self.connection = None

    def _connect(self):
        client = pymongo.MongoClient(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            authSource=self.auth_db,
            authMechanism="SCRAM-SHA-1",
        )
        db = client[self.db]
        self.connection = db[self.collection]

    # start function of api

    # This is function get data from mongoDB it's name "find"
    def find(self, sort_by, order):
        mongo_results = self.connection.find({})
        if sort_by is not None and order is not None:
            mongo_results.sort(sort_by, self._get_sort_by(order))
        return list(mongo_results)

    def _get_sort_by(self, sort: str) -> int:
        return pymongo.DESCENDING if sort == "desc" else pymongo.ASCENDING

    # This is function get method data for username that using
    def find_one(self, username):
        return self.connection.find_one({"_id": username})

    # This is function post method data for insert data
    def create(self, account: createAccountModel):
        account_dict = account.dict(exclude_unset=True)

        insert_dict = {**account_dict, "_id": account_dict["username"]}

        inserted_result = self.connection.insert_one(insert_dict)
        account_id = str(inserted_result.inserted_id)

        return account_id

    # This is function patch method for updata data
    def update(self, username, update_account: updateAccountModel):
        updated_result = self.connection.update_one(
            # query
            {"_id": username},
            # set value
            {"$set": update_account.dict(exclude_unset=True)},
        )
        return [username, updated_result.modified_count]

    # This is function delete method for delete data
    def delete(self, username):
        deleted_result = self.connection.delete_one({"username": username})
        return [username, deleted_result.deleted_count]

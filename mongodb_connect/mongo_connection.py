from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDBConnection:
    def __init__(self, database_name="tododb"):
        mongo_url = os.getenv("MONGO_URL")
        print(mongo_url)
        self.client = AsyncIOMotorClient(mongo_url,tlsAllowInvalidCertificates=True)
        self.database = self.client[database_name]

    def get_collection(self, collection_name):
        return self.database[collection_name]

mongodb_connection = MongoDBConnection()
user_collection = mongodb_connection.get_collection("users")
todo_collection = mongodb_connection.get_collection("todos")

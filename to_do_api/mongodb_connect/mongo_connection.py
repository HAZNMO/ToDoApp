from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class MongoDBConnection:
    def __init__(self, database_name="tododb"):
        mongo_url = os.getenv("MONGO_URL")

        if not mongo_url:
            logger.error("MONGO_URL is not set. Please check the environment variables.")
            raise ValueError("MONGO_URL is missing.")

        try:
            self.client = AsyncIOMotorClient(mongo_url, tlsAllowInvalidCertificates=True)
            self.database = self.client[database_name]
            logger.info(f"Connection to the database {database_name} established.")
        except Exception as e:
            logger.error(f"MongoDB connection error: {e}")
            raise ConnectionError("Failed to connect to MongoDB.") from e

    def get_collection(self, collection_name):
        try:
            collection = self.database[collection_name]
            logger.info(f"Collection '{collection_name}' retrieved successfully.")
            return collection
        except Exception as e:
            logger.error(f"Error retrieving the collection '{collection_name}': {e}")
            raise ValueError(f"Error accessing the collection '{collection_name}'") from e


mongodb_connection = MongoDBConnection()
user_collection = mongodb_connection.get_collection("users")
todo_collection = mongodb_connection.get_collection("todos")

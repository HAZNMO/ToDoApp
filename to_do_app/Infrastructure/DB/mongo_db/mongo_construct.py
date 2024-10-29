import logging
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)
load_dotenv()


class MongoDBConnection:
    def __init__(self, database_name="tododb"):
        mongo_url = os.getenv("MONGO_URL")

        if not mongo_url:
            error_message = (
                "MONGO_URL is not set. Please check the environment variables."
            )
            logger.error(error_message)
            missing_mongo_url_message = "MONGO_URL is missing."
            raise ValueError(missing_mongo_url_message)

        try:
            self.client = AsyncIOMotorClient(
                mongo_url, tlsAllowInvalidCertificates=True
            )
            self.database = self.client[database_name]
            logger.info("Connection to the database %s established.", database_name)
        except Exception as e:
            connection_error_message = "Failed to connect to MongoDB."
            logger.exception(connection_error_message)
            raise ConnectionError(connection_error_message) from e

    def get_collection(self, collection_name):
        try:
            collection = self.database[collection_name]
            logger.info("Collection '%s' retrieved successfully.", collection_name)
        except Exception:
            error_message = f"Error accessing the collection '{collection_name}'"
            logger.exception("%s: ", error_message)
            raise ValueError(error_message) from None
        else:
            return collection


mongodb_connection = MongoDBConnection()
user_collection = mongodb_connection.get_collection("users")
todo_collection = mongodb_connection.get_collection("todos")

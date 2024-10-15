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
            logger.error("MONGO_URL не установлен. Проверьте переменные окружения.")
            raise ValueError("Отсутствует MONGO_URL")

        try:
            self.client = AsyncIOMotorClient(mongo_url, tlsAllowInvalidCertificates=True)
            self.database = self.client[database_name]
            logger.info(f"Подключение к базе данных {database_name} установлено.")
        except Exception as e:
            logger.error(f"Ошибка подключения к MongoDB: {e}")
            raise ConnectionError("Не удалось подключиться к MongoDB") from e

    def get_collection(self, collection_name):
        try:
            collection = self.database[collection_name]
            logger.info(f"Коллекция '{collection_name}' успешно получена.")
            return collection
        except Exception as e:
            logger.error(f"Ошибка при получении коллекции '{collection_name}': {e}")
            raise ValueError(f"Ошибка при доступе к коллекции '{collection_name}'") from e


mongodb_connection = MongoDBConnection()
user_collection = mongodb_connection.get_collection("users")
todo_collection = mongodb_connection.get_collection("todos")

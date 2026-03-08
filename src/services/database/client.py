from loguru import logger
from pymongo import MongoClient

from services.database.config import mongodb_config


class MongoDBService:
    def __init__(self):
        self.client = MongoClient(
            mongodb_config.mongodb_host, mongodb_config.mongodb_port
        )
        try:
            self.client.admin.command("ping")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise
        self.database = self.client[mongodb_config.mongodb_database]

    def get_collection(self, name: str):
        try:
            return self.database[name]
        except Exception as e:
            logger.error(f"Error getting collection {name}: {e}")
            raise

    def insert_one(self, collection: str, document: dict):
        try:
            result = self.get_collection(collection).insert_one(document)
            logger.info(
                f"Successfully inserted one document into collection {collection}"
            )
            return result
        except Exception as e:
            logger.error(
                f"Error inserting one document into collection {collection}: {e}"
            )
            raise

    def insert_many(self, collection: str, documents: list[dict]):
        try:
            result = self.get_collection(collection).insert_many(documents)
            logger.info(
                f"Successfully inserted {len(result.inserted_ids)} documents into collection {collection}"
            )
            return result
        except Exception as e:
            logger.error(
                f"Error inserting many documents into collection {collection}: {e}"
            )
            raise

    def find_one(self, collection: str, query: dict):
        try:
            return self.get_collection(collection).find_one(query)
        except Exception as e:
            logger.error(f"Error finding one document in collection {collection}: {e}")
            raise

    def find_many(self, collection: str, query: dict):
        try:
            return self.get_collection(collection).find(query)
        except Exception as e:
            logger.error(
                f"Error finding many documents in collection {collection}: {e}"
            )
            raise

    def update_one(self, collection: str, query: dict, update: dict):
        try:
            result = self.get_collection(collection).update_one(query, update)
            logger.info(
                f"Successfully updated one document in collection {collection} "
                f"(matched {result.matched_count}, modified {result.modified_count})"
            )
            return result
        except Exception as e:
            logger.error(f"Error updating one document in collection {collection}: {e}")
            raise

    def update_many(self, collection: str, query: dict, update: dict):
        try:
            result = self.get_collection(collection).update_many(query, update)
            logger.info(
                f"Successfully updated documents in collection {collection} "
                f"(matched {result.matched_count}, modified {result.modified_count})"
            )
            return result
        except Exception as e:
            logger.error(
                f"Error updating many documents in collection {collection}: {e}"
            )
            raise

    def delete_one(self, collection: str, query: dict):
        try:
            result = self.get_collection(collection).delete_one(query)
            logger.info(
                f"Successfully deleted one document from collection {collection} "
                f"(deleted {result.deleted_count})"
            )
            return result
        except Exception as e:
            logger.error(f"Error deleting one document in collection {collection}: {e}")
            raise

    def delete_many(self, collection: str, query: dict):
        try:
            result = self.get_collection(collection).delete_many(query)
            logger.info(
                f"Successfully deleted documents from collection {collection} "
                f"(deleted {result.deleted_count})"
            )
            return result
        except Exception as e:
            logger.error(
                f"Error deleting many documents in collection {collection}: {e}"
            )
            raise

from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from pymongo import TEXT
from utils.logger_utils import Logger

# Initialize the logger
logger = Logger().get_logger()

def insert_document(collection: Collection, document: dict) -> bool:
    """Insert a single document into a MongoDB collection."""
    try:
        result = collection.insert_one(document)
        logger.info(f"Document inserted with ID: {result.inserted_id}")
        return True
    except PyMongoError as e:
        logger.error(f"Failed to insert document: {e}")
        return False

def find_documents(collection: Collection, query: dict, limit: int = 0) -> list:
    """Find documents in a MongoDB collection that match a query."""
    try:
        # Apply the limit if it's greater than 0
        cursor = collection.find(query)
        if limit > 0:
            cursor = cursor.limit(limit)
        documents = list(cursor)
        logger.info(f"Found {len(documents)} documents matching the query.")
        return documents
    except PyMongoError as e:
        logger.error(f"Failed to find documents: {e}")
        return []

def update_documents(collection: Collection, query: dict, update: dict) -> int:
    """Update documents in a MongoDB collection that match a query."""
    try:
        result = collection.update_many(query, {'$set': update})
        logger.info(f"Updated {result.modified_count} documents.")
        return result.modified_count
    except PyMongoError as e:
        logger.error(f"Failed to update documents: {e}")
        return 0

def delete_documents(collection: Collection, query: dict) -> int:
    """Delete documents from a MongoDB collection that match a query."""
    try:
        result = collection.delete_many(query)
        logger.info(f"Deleted {result.deleted_count} documents.")
        return result.deleted_count
    except PyMongoError as e:
        logger.error(f"Failed to delete documents: {e}")
        return 0

def create_text_index(collection: Collection, fields: list) -> bool:
    """Create a text index on specified fields for fuzzy search."""
    try:
        collection.create_index([(field, TEXT) for field in fields])
        logger.info(f"Text index created on fields: {fields}")
        return True
    except PyMongoError as e:
        logger.error(f"Failed to create text index: {e}")
        return False

def fuzzy_search(collection: Collection, search_text: str, field: str) -> list:
    """Perform a fuzzy search using a regex on a specific field."""
    try:
        # Use a case-insensitive regex search on the specified field
        query = {field: {"$regex": search_text, "$options": "i"}}
        documents = list(collection.find(query))
        logger.info(f"Found {len(documents)} documents matching the search text in field '{field}'.")
        return documents
    except PyMongoError as e:
        logger.error(f"Failed to perform fuzzy search: {e}")
        return []

def aggregate_documents(collection: Collection, pipeline: list) -> list:
    """Perform an aggregation operation using a pipeline."""
    try:
        results = list(collection.aggregate(pipeline))
        logger.info(f"Aggregation returned {len(results)} results.")
        return results
    except PyMongoError as e:
        logger.error(f"Failed to perform aggregation: {e}")
        return []

def count_documents(collection: Collection, query: dict) -> int:
    """Count the number of documents matching a query."""
    try:
        count = collection.count_documents(query)
        logger.info(f"Counted {count} documents matching the query.")
        return count
    except PyMongoError as e:
        logger.error(f"Failed to count documents: {e}")
        return 0

def distinct_values(collection: Collection, field: str) -> list:
    """Get distinct values for a specified field."""
    try:
        values = collection.distinct(field)
        logger.info(f"Found {len(values)} distinct values for field '{field}'.")
        return values
    except PyMongoError as e:
        logger.error(f"Failed to get distinct values: {e}")
        return []
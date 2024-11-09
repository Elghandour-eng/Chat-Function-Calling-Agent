from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from utils.logger_utils import Logger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the logger
logger = Logger().get_logger()

class MongoDBClient:
    _instance = None

    def __new__(cls, uri, db_name, max_pool_size=100, min_pool_size=0):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance._initialize(uri, db_name, max_pool_size, min_pool_size)
        return cls._instance

    def _initialize(self, uri, db_name, max_pool_size, min_pool_size):
        self._uri = uri
        self._db_name = db_name
        self._client = None
        self._db = None
        self._max_pool_size = max_pool_size
        self._min_pool_size = min_pool_size
        self._connect()

    def _connect(self):
        try:
            self._client = MongoClient(
                self._uri,
                maxPoolSize=self._max_pool_size,
                minPoolSize=self._min_pool_size
            )
            self._client.admin.command('ping')
            self._db = self._client[self._db_name]
            logger.info("Connected to MongoDB successfully.")
        except (ConnectionFailure, ConfigurationError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def get_database(self):
        return self._db

    def get_collection(self, collection_name: str):
        """Get a specific collection from the database."""
        if self._db is not None:
            return self._db[collection_name]
        else:
            logger.error("Database connection is not established.")
            raise ConnectionFailure("Database connection is not established.")

    def close_connection(self):
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed.")


import os
from flask import Blueprint, request, jsonify
from database.mongodb_client import MongoDBClient
from database.mongodb_utils import find_documents, fuzzy_search, aggregate_documents
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

purchase_order_bp = Blueprint('purchase_order', __name__)

# Retrieve environment variables
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME", "purchase_orders")  # Default to 'purchase_orders'

# Initialize MongoDB client
mongo_client = MongoDBClient(mongo_uri, db_name)
collection = mongo_client.get_collection(collection_name)

def serialize_document(doc):
    """Convert MongoDB document to a JSON-serializable dictionary."""
    if isinstance(doc, dict):
        return {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in doc.items()}
    return doc

@purchase_order_bp.route('/', methods=['GET'])
def get_all_purchase_orders():
    """Get all purchase orders."""
    query = request.args.to_dict()  # Convert query parameters to a dictionary
    purchase_orders = find_documents(collection, query)
    serialized_orders = [serialize_document(order) for order in purchase_orders]
    return jsonify(serialized_orders), 200

@purchase_order_bp.route('/first-six', methods=['GET'])
def get_first_six_purchase_orders():
    """Get the first six purchase orders."""
    purchase_orders = find_documents(collection, {}, limit=6)
    serialized_orders = [serialize_document(order) for order in purchase_orders]
    return jsonify(serialized_orders), 200

@purchase_order_bp.route('/search', methods=['GET'])
def search_purchase_orders():
    """Perform a fuzzy search on purchase orders."""
    search_text = request.args.get('q', '')
    purchase_orders = fuzzy_search(collection, search_text)
    serialized_orders = [serialize_document(order) for order in purchase_orders]
    return jsonify(serialized_orders), 200

@purchase_order_bp.route('/aggregate', methods=['POST'])
def aggregate_purchase_orders():
    """Perform an aggregation on purchase orders."""
    pipeline = request.json.get('pipeline', [])
    results = aggregate_documents(collection, pipeline)
    serialized_results = [serialize_document(result) for result in results]
    return jsonify(serialized_results), 200
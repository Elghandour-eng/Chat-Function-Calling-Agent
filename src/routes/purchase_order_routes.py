import os
import json
from flask import Blueprint, request, jsonify
from bson import ObjectId
from dotenv import load_dotenv

from database.mongodb_client import MongoDBClient
from database.mongodb_utils import find_documents, fuzzy_search, aggregate_documents
from llms.azure_openai_client import ask_openai
from utils.query_parser import parse_query
from utils.prompt import get_prompt  # Importing the prompt

# Load environment variables from .env file
load_dotenv()

# Initialize Blueprint and environment variables
purchase_order_bp = Blueprint('purchase_order', __name__)
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME", "Pipeline")  # Default to 'Pipeline'

# Initialize MongoDB client
mongo_client = MongoDBClient(mongo_uri, db_name)
collection = mongo_client.get_collection(collection_name)

def serialize_document(doc):
    """Convert MongoDB document to a JSON-serializable dictionary."""
    if isinstance(doc, dict):
        return {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in doc.items()}
    return doc

# --- Routes for Purchase Orders CRUD and Aggregation Operations ---

@purchase_order_bp.route('/', methods=['GET'])
def get_all_purchase_orders():
    """Retrieve all purchase orders with optional query filtering."""
    query = request.args.to_dict()
    purchase_orders = find_documents(collection, query)
    serialized_orders = [serialize_document(order) for order in purchase_orders]
    return jsonify(serialized_orders), 200

@purchase_order_bp.route('/first-six', methods=['GET'])
def get_first_six_purchase_orders():
    """Retrieve the first six purchase orders."""
    purchase_orders = find_documents(collection, {}, limit=6)
    serialized_orders = [serialize_document(order) for order in purchase_orders]
    return jsonify(serialized_orders), 200

@purchase_order_bp.route('/search', methods=['GET'])
def search_purchase_orders():
    """Perform a fuzzy search on purchase orders by a search text."""
    search_text = request.args.get('q', '')
    purchase_orders = fuzzy_search(collection, search_text)
    serialized_orders = [serialize_document(order) for order in purchase_orders]
    return jsonify(serialized_orders), 200

@purchase_order_bp.route('/aggregate', methods=['POST'])
def aggregate_purchase_orders():
    """Execute an aggregation pipeline on purchase orders."""
    pipeline = request.json.get('pipeline', [])
    results = aggregate_documents(collection, pipeline)
    serialized_results = [serialize_document(result) for result in results]
    return jsonify(serialized_results), 200

# --- AI Interaction Route ---

@purchase_order_bp.route('/ask', methods=['POST'])
def ask_question():
    """Handle a natural language question and interact with the database."""
    data = request.json
    question = data.get("question", "")
    prompt = get_prompt()

    response_message = ask_openai(question, prompt)

    if isinstance(response_message, dict):
        return jsonify({"answer": response_message['answer']}), 200
    else:
        return jsonify({"answer": response_message}), 200

@purchase_order_bp.route('/filter', methods=['GET'])
def filter_purchase_orders():
    """Filter purchase orders based on query parameters with special parsing."""
    query = request.args.to_dict()
    parsed_query = parse_query(query)  # Apply the custom query parser for fields like fiscal year
    purchase_orders = find_documents(collection, parsed_query)
    serialized_orders = [serialize_document(order) for order in purchase_orders]
    return jsonify(serialized_orders), 200



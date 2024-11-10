import os
import json
from flask import Blueprint, request, jsonify, session
from bson import ObjectId
from dotenv import load_dotenv

from database.mongodb_client import MongoDBClient
from database.mongodb_utils import find_documents, fuzzy_search, aggregate_documents
from llms.azure_openai_client import ask_openai
from utils.query_parser import parse_query
from utils.prompt import get_prompt  # Importing the prompt
from utils.logger_utils import Logger

logging = Logger().get_logger()

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
    """Perform a fuzzy search on purchase orders by a search text and field."""
    field = request.args.get('field', '')
    search_text = request.args.get('q', '')

    if not field or not search_text:
        return jsonify({"error": "Field and search text are required"}), 400

    # Implement your fuzzy search logic here, using the specified field
    purchase_orders = fuzzy_search(collection, field, search_text)
    serialized_orders = [serialize_document(order) for order in purchase_orders]
    return jsonify(serialized_orders), 200

@purchase_order_bp.route('/aggregate', methods=['POST'])
def aggregate_purchase_orders():
    """Execute an aggregation pipeline on purchase orders."""
    pipeline = request.json.get('pipeline', [])
    logging.info(f"Received pipeline: {pipeline}")  # Log the pipeline
    results = aggregate_documents(collection, pipeline)
    serialized_results = [serialize_document(result) for result in results]
    return jsonify(serialized_results), 200


# @purchase_order_bp.route('/chat', methods=['POST'])
# def query_purchase_orders():
#     """Interpret a natural language query and retrieve matching purchase orders."""
#     data = request.json
#     user_query = data.get('query', '')
    
#     if not user_query:
#         logging.error("Query text is required.")
#         return jsonify({"error": "Query text is required"}), 400
    
#     # Get the prompt and pass it along with the user query to OpenAI
#     interpreted_query = ask_openai(user_query, get_prompt())
#     logging.info(interpreted_query)
    

#     if "answer" not in interpreted_query:
#         logging.error("Failed to get a valid response from OpenAI.")
#         return jsonify({"error": "Failed to get a valid response from OpenAI."}), 500

    
#     if "error" in interpreted_query:
#         logging.error(f"Error from OpenAI: {interpreted_query['error']}")
#         return jsonify(interpreted_query), 500

#     logging.info("Retrieved response from OpenAI successfully.")
    
#     return jsonify(interpreted_query), 200



@purchase_order_bp.route('/chat', methods=['POST'])
def query_purchase_orders():
    """Interpret a natural language query and retrieve matching purchase orders."""
    data = request.json
    user_query = data.get('query', '')
    
    if not user_query:
        logging.error("Query text is required.")
        return jsonify({"error": "Query text is required"}), 400
    
    # Retrieve the conversation history from the session
    messages = session.get('messages', [])
    
    # Get the prompt and pass it along with the user query to OpenAI
    interpreted_query = ask_openai(user_query, get_prompt(), messages)
    logging.info(interpreted_query)
    
    if "answer" not in interpreted_query:
        logging.error("Failed to get a valid response from OpenAI.")
        return jsonify({"error": "Failed to get a valid response from OpenAI."}), 500

    if "error" in interpreted_query:
        logging.error(f"Error from OpenAI: {interpreted_query['error']}")
        return jsonify(interpreted_query), 500

    logging.info("Retrieved response from OpenAI successfully.")
    
    # Save the updated conversation history back to the session
    session['messages'] = messages
    
    return jsonify(interpreted_query), 200
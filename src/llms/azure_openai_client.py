import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from database.mongodb_client import MongoDBClient
from database.mongodb_utils import find_documents
from utils.serialization import serialize_document

# Load environment variables
load_dotenv()

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview"
)
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

# Initialize MongoDB Client
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")
mongo_client = MongoDBClient(mongo_uri, db_name)
collection = mongo_client.get_collection("purchase_orders")  # Make sure to use the correct collection name

def load_functions():
    """Load function definitions from functions.json."""
    functions_path = os.path.join(os.path.dirname(__file__), "functions.json")
    with open(functions_path, "r") as file:
        functions = json.load(file)
    return list(functions.values())

def ask_openai(question, prompt):
    """Send question and prompt to Azure OpenAI and return the response."""
    context = [{"role": "user", "content": question}]
    tools = load_functions()  # Load function definitions

    # Add the prompt to the context
    context.insert(0, {"role": "system", "content": prompt})

    # Pass the correct function call
    response = client.chat.completions.create(
        model=deployment_name,
        messages=context,
        tools=tools,  # Pass the loaded function definitions
        tool_choice="auto",
    )

    # If the tool call is suggested by the model, it will include 'tool_calls'
    if response.choices[0].message.get('tool_calls'):
        tool_call = response.choices[0].message['tool_calls'][0]
        function_name = tool_call['function']['name']
        function_args = tool_call['function']['arguments']

        # Perform the tool call here, e.g., fetch data from MongoDB
        if function_name == "fetch_purchase_order_data":
            query = json.loads(function_args.get("query"))
            documents = find_documents(collection, query)  # Ensure collection is defined
            serialized_docs = [serialize_document(doc) for doc in documents]
            return {"answer": serialized_docs}  # Return MongoDB results

    # If no tool call is needed, return the response content directly
    return response.choices[0].message['content']

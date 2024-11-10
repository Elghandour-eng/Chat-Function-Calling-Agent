import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from database.mongodb_client import MongoDBClient
from database.mongodb_utils import find_documents, aggregate_documents
from utils.serialization import serialize_document
from utils.logger_utils import Logger
import requests

# Load environment variables
load_dotenv()


logging = Logger().get_logger()
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
collection = mongo_client.get_collection("purchase_orders")  # Ensure correct collection name


# def ask_openai(question, prompt):
#     """Send question and prompt to Azure OpenAI and return the response."""
#     logging.info(f"Received question: {question}")

#     context = [{"role": "user", "content": question}]
#     tools = [
#         {
#             "type": "function",
#             "function": {
#                 "name": "get_all_purchase_orders",
#                 "description": "Retrieve all purchase orders",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {}
#                 }
#             }
#         },
#         {
#             "type": "function",
#             "function": {
#                 "name": "get_first_six_purchase_orders",
#                 "description": "Retrieve the first six purchase orders",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {}
#                 }
#             }
#         },
#         {
#             "type": "function",
#             "function": {
#                 "name": "search_purchase_orders",
#                 "description": "Perform a fuzzy search on purchase orders",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "search_text": {
#                             "type": "string",
#                             "description": "Text to search for in purchase orders"
#                         }
#                     },
#                     "required": ["search_text"]
#                 }
#             }
#         },
#         {
#             "type": "function",
#             "function": {
#                 "name": "aggregate_purchase_orders",
#                 "description": "Execute an aggregation pipeline on purchase orders",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "pipeline": {
#                             "type": "array",
#                             "description": "Aggregation pipeline steps",
#                             "items": {
#                                 "type": "object"
#                             }
#                         }
#                     },
#                     "required": ["pipeline"]
#                 }
#             }
#         }
#     ]

#     # Add the prompt to the context
#     context.insert(0, {"role": "system", "content": prompt})

#     try:
#         # Send the query and context to OpenAI for processing
#         logging.info("Sending query to OpenAI for processing...")
#         response = client.chat.completions.create(
#             model=deployment_name,
#             messages=context,
#             tools=tools,  # Pass the tools as defined above
#             tool_choice="auto",
#         )

#         # Log OpenAI response
#         logging.info(f"OpenAI response: {response.choices}")
#         response_message = response.choices[0].message
           

#         # Check if OpenAI suggests using a tool
#         if response_message.tool_calls:
#             for tool_call in response_message.tool_calls:
#                 function_name = tool_call.function.name
#                 function_args = json.loads(tool_call.function.arguments)
#                 print(f"Function call: {function_name}")  
#                 print(f"Function arguments: {function_args}")  

#             # Define Flask API URL (make sure to use the correct base URL)
#             flask_base_url = "http://127.0.0.1:5000/api/purchase_orders"  # Replace with actual URL of your Flask app
#             api_url = ""

#             # Based on the tool name, call the corresponding API endpoint
#             if function_name == "get_all_purchase_orders":
#                 api_url = f"{flask_base_url}/"
#                 response = requests.get(api_url, params=function_args)
#                 logging.info(response)
#             elif function_name == "get_first_six_purchase_orders":
#                 api_url = f"{flask_base_url}/first-six"
#                 response = requests.get(api_url, params=function_args)
#                 # logging.info(f"resonse re{response}")
#             elif function_name == "search_purchase_orders":
#                 api_url = f"{flask_base_url}/search"
#                 response = requests.get(api_url, params=function_args)
#             elif function_name == "aggregate_purchase_orders":
#                 api_url = f"{flask_base_url}/aggregate"
#                 response = requests.post(api_url, json=function_args)
            
#             # Log the API response from Flask
#             # logging.info(f"Flask API response from {api_url}: {response}")
            
#             # If the response is successful, return the data
#             if response:
#                 data = response.json()
#                 # logging.info(f"API Response Data: {data}")
#                 return {"answer": data}  # Return MongoDB results as part of OpenAI's response
#             else:
#                 logging.error(f"Error calling Flask API: {response}, {response}")
#                 return {"error": f"Failed to fetch data from Flask API. Status code: {response}"}
        
#         else:
#             # If no tool call was made, just return the response message from OpenAI
#             return {"answer": response.choices[0].message.content}

#     except Exception as e:
#         logging.error(f"Error occurred during OpenAI interaction: {str(e)}")
#         return {"error": str(e)}


def ask_openai(question, prompt, messages):
    """Send question and prompt to Azure OpenAI and return the response."""
    logging.info(f"Received question: {question}")

    if not messages:
        messages.append({"role": "system", "content": prompt})
    messages.append({"role": "user", "content": question})

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_all_purchase_orders",
                "description": "Retrieve all purchase orders",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_first_six_purchase_orders",
                "description": "Retrieve the first six purchase orders",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_purchase_orders",
                "description": "Perform a fuzzy search on purchase orders by a search text and field don't pass from other always pass both.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "field": {
                            "type": "string",
                            "description": "The field to search within purchase orders"
                        },
                        "q": {
                            "type": "string",
                            "description": "Text query to search for in purchase orders"
                        }
                    },
                    "required": ["field", "q"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "aggregate_purchase_orders",
                "description": "Execute an aggregation pipeline on purchase orders",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pipeline": {
                            "type": "array",
                            "description": "Aggregation pipeline steps try to parse user queries like give me count of document for example in day to pipeline steps matching with mongo ",
                            "items": {
                                "type": "object"
                            }
                        }
                    },
                    "required": ["pipeline"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "general_inquiry",
                "description": "Generate a MongoDB aggregation pipeline from user inquiry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "inquiry": {
                            "type": "string",
                            "description": "User inquiry to generate a pipeline"
                        }
                    },
                    "required": ["inquiry"]
                }
            }
        }
    ]

    try:
        logging.info("Sending query to OpenAI for processing...")
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        response_message = response.choices[0].message.to_dict()
        messages.append(response_message)

        if response_message.get('tool_calls'):
            for tool_call in response_message['tool_calls']:
                function_name = tool_call['function']['name']
                function_args = json.loads(tool_call['function']['arguments'])
                print(f"Function call: {function_name}")  
                print(f"Function arguments: {function_args}")  

                flask_base_url = "http://127.0.0.1:5000/api/purchase_orders"
                api_url = ""

                if function_name == "get_all_purchase_orders":
                    api_url = f"{flask_base_url}/"
                    response = requests.get(api_url, params=function_args)
                elif function_name == "get_first_six_purchase_orders":
                    api_url = f"{flask_base_url}/first-six"
                    response = requests.get(api_url, params=function_args)
                elif function_name == "search_purchase_orders":
                    api_url = f"{flask_base_url}/search"
                    response = requests.get(api_url, params=function_args)
                elif function_name == "aggregate_purchase_orders":
                    api_url = f"{flask_base_url}/aggregate"
                    response = requests.post(api_url, json=function_args)
                elif function_name == "general_inquiry":
                    logging.info("Generating pipeline for general inquiry...")
                    try:
                        inquiry_prompt = (
            "You are a helpful assistant that creates MongoDB aggregation pipelines.  don't include ``` json at first or ``` at end"
            "Do not include markdown formatting like json at the beginning or end of your response. "
            "Here are some examples and details to help you create a good pipeline:\n\n"
            "- **Fiscal Year**: Encoded as `0` for 2012-2013, `1` for 2013-2014, and `2` for 2014-2015.\n"
            "- **Creation Date**: System-generated date marking when data is entered.\n"
            "- **Purchase Date**: Actual date of purchase as recorded by the user.\n"
            "- **Fiscal Year**: Derived based on the creation date, following California's fiscal cycle (July 1 - June 30).\n"
            "- **LPA Number**: Contract or Leveraged Procurement Agreement (LPA) Number, marking contract dollars.\n"
            "- **Purchase Order Number**: Unique to each purchase order but can be duplicated across departments.\n"
            "- **Requisition Number**: Unique to each requisition, though duplicable across departments.\n"
            "- **Acquisition Type & Method**: Categories of acquisition (IT vs. Non-IT Goods/Services) and procurement method used.\n"
            "- **Department Name**: Identifies the purchasing department.\n"
            "- **Supplier Details**: Include supplier code, name, qualifications, and zip code.\n"
            "- **CalCard Usage**: Marks if a state-issued credit card was used.\n"
            "- **Item Details**: Include item name, description, quantity, unit price, and total price.\n"
            "- **UNSPSC Classification Codes**: An 8-digit normalized United Nations Standard Products and Services Code (UNSPSC) for items, along with correlated commodity title, class, family, and segment information.\n\n"
            "Create a pipeline for the following inquiry: "
            f"{function_args['inquiry']}"
        )
                        pipeline_response = client.chat.completions.create(
                            model=deployment_name,
                                       messages=[
                {"role": "system", "content": inquiry_prompt},
                {"role": "user", "content": function_args['inquiry']}
            ]
                        )
                        generated_pipeline = pipeline_response.choices[0].message.content
                        logging.info(f"Generated pipeline: {generated_pipeline}")
                        pipeline_json = json.loads(generated_pipeline)
                        api_url = f"{flask_base_url}/aggregate"
                        response = requests.post(api_url, json={"pipeline": pipeline_json})
                    except Exception as e:
                        logging.error(f"Error generating pipeline: {str(e)}")
                        messages.append({
                            "tool_call_id": tool_call['id'],
                            "role": "tool",
                            "name": function_name,
                            "content": "not found"
                        })
                        continue

                if response.status_code in [400, 500]:
                    logging.error(f"Error calling Flask API: {response.status_code}")
                    messages.append({
                        "tool_call_id": tool_call['id'],
                        "role": "tool",
                        "name": function_name,
                        "content": "not found"
                    })
                else:
                    data = response.json()
                    messages.append({
                        "tool_call_id": tool_call['id'],
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(data),
                    })

        final_response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
        )

        return {"answer": final_response.choices[0].message.content}

    except Exception as e:
        logging.error(f"Error occurred during OpenAI interaction: {str(e)}")
        return {"answer": "not found"}

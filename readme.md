# Project Overview

This project is a native application utilizing Azure and function calling to retrieve data from a MongoDB database.

## File Structure

```
└── 📁src
    ├── 📁database
    │   ├── 📁__pycache__
    │   │   ├── mongodb_client.cpython-312.pyc
    │   │   └── mongodb_utils.cpython-312.pyc
    │   ├── mongodb_client.py
    │   └── mongodb_utils.py
    ├── 📁llms
    │   ├── 📁__pycache__
    │   │   └── azure_openai_client.cpython-312.pyc
    │   ├── azure_openai_client.py
    │   └── functions.json
    ├── 📁models
    │   └── purchase_order.py
    ├── 📁routes
    │   ├── 📁__pycache__
    │   │   └── purchase_order_routes.cpython-312.pyc
    │   ├── collection.json
    │   └── purchase_order_routes.py
    ├── 📁utils
    │   ├── 📁__pycache__
    │   │   ├── logger_utils.cpython-312.pyc
    │   │   ├── prompt.cpython-312.pyc
    │   │   ├── query_parser.cpython-312.pyc
    │   │   └── serialization.cpython-312.pyc
    │   ├── logger_utils.py
    │   ├── prompt.py
    │   ├── query_parser.py
    │   └── serialization.py
    └── main.py
```



## Setup Instructions

1. **Environment Configuration:**

   Copy the `example.env` file and update it with your Azure and MongoDB credentials:

   ```plaintext
   MONGO_URI=mongodb://<username>:<password>@localhost:27017

   # Name of the database to use
   DB_NAME=my_database
   COLLECTION_NAME=collection_name

   # Optional: Log file path and log level
   LOG_FILE=app.log
   LOG_LEVEL=INFO

   # AZURE
   AZURE_OPENAI_ENDPOINT="your_azure_endpoint"
   AZURE_OPENAI_API_KEY="your_api_key"
   AZURE_DEPLOYMENT_NAME="your_deployment_name"
   ```

2. **Install Dependencies:**

   Make sure to install the required dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Once the environment is set up and dependencies are installed, you can run the project using:

```bash
python src/main.py
```

Ensure that your environment variables are correctly set up to connect to your MongoDB and Azure services.
import threading
from flask import Flask, request, jsonify, session
from routes.purchase_order_routes import purchase_order_bp
import gradio as gr
import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Flask app initialization
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key'  # Replace with a strong, random key

# Register the blueprint for the purchase order routes
app.register_blueprint(purchase_order_bp, url_prefix='/api/purchase_orders')

# Start Flask API server in a separate thread
def run_flask():
    app.run(debug=True, use_reloader=False, port=5000)  # Disable reloader to avoid issues with threading

# Gradio app initialization
FLASK_URL = "http://127.0.0.1:5000/api/purchase_orders/chat"

# Create a session for persistent cookies
session = requests.Session()

def query_chat(user_query):
    # Send a POST request to the Flask app's chat route, maintaining session cookies
    payload = {"query": user_query}
    headers = {"Content-Type": "application/json"}

    try:
        response = session.post(FLASK_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("answer", "No answer found")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def add_message(history, message):
    for x in message["files"]:
        history.append({"role": "user", "content": {"path": x}})
    if message["text"] is not None:
        history.append({"role": "user", "content": message["text"]})
    return history, gr.MultimodalTextbox(value=None, interactive=False)

def bot(history: list):
    user_query = history[-1]["content"]
    response = query_chat(user_query)
    history.append({"role": "assistant", "content": ""})
    for character in response:
        history[-1]["content"] += character
        time.sleep(0.05)
        yield history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(elem_id="chatbot", bubble_full_width=False, type="messages")

    chat_input = gr.MultimodalTextbox(
        interactive=True,
        file_count="multiple",
        placeholder="Enter message or upload file...",
        show_label=False,
    )

    chat_msg = chat_input.submit(
        add_message, [chatbot, chat_input], [chatbot, chat_input]
    )
    bot_msg = chat_msg.then(bot, chatbot, chatbot, api_name="bot_response")
    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

    chatbot.like(print_like_dislike, None, None, like_user_message=True)

# Start Gradio in the main thread
def run_gradio():
    demo.launch(share=True)  # share=True to generate a public link (optional)

# Run both Flask and Gradio servers in parallel
if __name__ == "__main__":
    # Create a thread for Flask
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Run Gradio in the main thread
    run_gradio()
from flask import Flask
from routes.purchase_order_routes import purchase_order_bp

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key'  # Replace with a strong, random key

app.register_blueprint(purchase_order_bp, url_prefix='/api/purchase_orders')

if __name__ == '__main__':
    app.run(debug=True)
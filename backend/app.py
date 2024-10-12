import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

# Vytvoření a konfigurace aplikace
app = Flask(__name__)
CORS(app)

# Připojení k MongoDB
client = MongoClient("mongodb://admin:password@mongo-db:27017/")  # Připojení s uživatelským jménem a heslem
db = client.mydatabase  # Název databáze

# Konfigurace logování
logging.basicConfig(
    filename='app.log',  # Zde zvolíš cestu pro logovací soubor
    level=logging.INFO,   # Úroveň logování (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formát logovacích zpráv
)

@app.route('/')
def hello_world():
    app.logger.info('Zpráva pro logování: Hello, World!')  # Logování zprávy
    return 'Hello, World!'

# Příklad CRUD operací
@app.route('/items', methods=['GET'])
def get_items():
    items = list(db.items.find())
    for item in items:
        item['_id'] = str(item['_id'])  # Převod ObjectId na string
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    db.items.insert_one(data)
    return jsonify({"message": "Item added successfully!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8007, debug=True)  # Port 3000, jak je uvedeno v docker-compose.yml

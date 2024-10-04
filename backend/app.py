import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Vytvoření a konfigurace aplikace
app = Flask(__name__)
CORS(app)

# Konfigurace připojení k SQLite databázi (lokálně uložený soubor)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializace databáze
db = SQLAlchemy(app)

# Konfigurace logování
logging.basicConfig(
    filename='/app/logs/app.log',  # Cesta pro logovací soubor (v Dockeru bude namapováno přes volume)
    level=logging.INFO,   # Úroveň logování
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formát logovacích zpráv
)

# Definice modelu (tabulky)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/')
def hello_world():
    app.logger.info('Zpráva pro logování: Hello, World!')  # Logování zprávy
    return 'Hello, World!'

# Vytvoření tabulek v databázi při prvním spuštění
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8007, debug=True)

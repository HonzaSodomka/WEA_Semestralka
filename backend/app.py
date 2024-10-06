import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Vytvoření a konfigurace aplikace
app = Flask(__name__)
CORS(app)

# Konfigurace připojení k databázi SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite databáze
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Vytvoření instance SQLAlchemy
db = SQLAlchemy(app)

# Definice modelu
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

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

# Vytvoření tabulek v databázi
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8007, debug=True)

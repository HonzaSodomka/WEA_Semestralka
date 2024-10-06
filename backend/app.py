import logging
from flask import Flask, render_template
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
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

# Konfigurace logování
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
def catalog():
    # Příklad knih (můžete to nahradit databází nebo jiným způsobem získání dat)
    books = [
        {"title": "Kniha 1", "price": 199.99, "image_url": " "},
        {"title": "Kniha 2", "price": 249.99, "image_url": " "},
        {"title": "Kniha 3", "price": 299.99, "image_url": " "},
        {"title": "Kniha 4", "price": 349.99, "image_url": " "},
    ]
    
    return render_template('catalog.html', books=books)

# Vytvoření tabulek v databázi
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8007, debug=True)

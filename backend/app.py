from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'

    ISBN10 = db.Column(db.String(10), primary_key=True)
    ISBN13 = db.Column(db.String(13), unique=True, nullable=False)
    Title = db.Column(db.String(255), nullable=False)
    Author = db.Column(db.String(255), nullable=False)
    Genres = db.Column(db.String(255))
    Cover_Image = db.Column(db.String(255))
    Critics_Rating = db.Column(db.Float)
    Year_of_Publication = db.Column(db.Integer)
    Number_of_Pages = db.Column(db.Integer)
    Average_Customer_Rating = db.Column(db.Float)
    Number_of_Ratings = db.Column(db.Integer)

def add_book(isbn10, isbn13, title, author, genres=None, cover_image=None, critics_rating=None, 
             year_of_publication=None, number_of_pages=None, average_customer_rating=None, number_of_ratings=None):
    try:
        new_book = Book(
            ISBN10=isbn10,
            ISBN13=isbn13,
            Title=title,
            Author=author,
            Genres=genres,
            Cover_Image=cover_image,
            Critics_Rating=critics_rating,
            Year_of_Publication=year_of_publication,
            Number_of_Pages=number_of_pages,
            Average_Customer_Rating=average_customer_rating,
            Number_of_Ratings=number_of_ratings
        )
        db.session.add(new_book)
        db.session.commit()
        return True, "Book added successfully"
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)

def get_all_books():
    try:
        books = Book.query.all()
        return books
    except SQLAlchemyError as e:
        return None

@app.route('/api/books')
def get_books():
    books = get_all_books()
    if books is None:
        return jsonify({'error': 'Nepodařilo se získat knihy'}), 500

    return jsonify([
        {
            'ISBN10': book.ISBN10,
            'ISBN13': book.ISBN13,
            'Title': book.Title,
            'Author': book.Author,
            'Genres': book.Genres,
            'Cover_Image': book.Cover_Image,
            'Critics_Rating': book.Critics_Rating,
            'Year_of_Publication': book.Year_of_Publication,
            'Number_of_Pages': book.Number_of_Pages,
            'Average_Customer_Rating': book.Average_Customer_Rating,
            'Number_of_Ratings': book.Number_of_Ratings
        } for book in books
    ])

@app.route('/api/import_mock_books')
def import_mock_books():
    df = pd.read_csv('data_mock.csv', header=None)
    
    # Vymazání starých knih
    db.session.query(Book).delete()
    
    for index, row in df.iterrows():
        add_book(
            isbn10=row[1],
            isbn13=row[0],
            title=row[2],
            author=row[4],
            genres=row[5],
            cover_image=row[6],
            critics_rating=row[8],
            year_of_publication=row[7],
            number_of_pages=row[9],
            average_customer_rating=row[10],
            number_of_ratings=row[11]
        )

    return jsonify({'message': f'Imported {len(df)} books.'})

@app.route('/api/import_books_from_cdb', methods=['POST'])
def import_books_from_cdb():
    response = requests.post('http://wea.nti.tul.cz:1337/data', headers={'accept': '*/*', 'Content-Type': 'application/json'})
    data = response.json()

    # Vymazání starých knih
    db.session.query(Book).delete()

    for item in data:
        add_book(
            isbn10=item['isbn10'],
            isbn13=item['isbn13'],
            title=item['title'],
            author=item['authors'],
            genres=item['categories'],
            cover_image=item['thumbnail'],
            critics_rating=item.get('average_rating'),
            year_of_publication=item.get('published_year'),
            number_of_pages=item.get('num_pages'),
            average_customer_rating=None,  # Předpokládáme, že není v datech
            number_of_ratings=None  # Předpokládáme, že není v datech
        )

    return jsonify({'message': 'Books imported from CDB successfully.'})

if __name__ == '__main__':
    app.run(port=8007)

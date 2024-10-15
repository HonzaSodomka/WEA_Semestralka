from database.models import db, Book
from sqlalchemy.exc import SQLAlchemyError

# Funkce pro přidání knihy do databáze
def add_book(isbn10, isbn13, title, author, genres=None, cover_image=None, 
             year_of_publication=None, number_of_pages=None, average_customer_rating=None, number_of_ratings=None):
    try:
        # Zkontrolujeme, zda kniha již neexistuje podle ISBN13
        existing_book = Book.query.filter_by(ISBN13=isbn13).first()
        if existing_book:
            return False, "Book already exists in the database"

        new_book = Book(
            ISBN10=isbn10,
            ISBN13=isbn13,
            Title=title,
            Author=author,
            Genres=genres,
            Cover_Image=cover_image,
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

# Funkce pro získání všech knih z databáze
def get_all_books():
    try:
        return Book.query.all()
    except SQLAlchemyError as e:
        return None

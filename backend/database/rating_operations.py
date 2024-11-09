# rating_operations.py
from sqlalchemy.exc import SQLAlchemyError
from database.book import Book
from database.rating import Rating
from database import db

def add_or_update_rating(book_isbn10, user_id, rating_value):
    """
    Add or update a user's rating for a book and update the book's average rating.
    
    Args:
        book_isbn10 (str): The book's ISBN10
        user_id (int): The user's ID
        rating_value (int): Rating value (1-5)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        if not 1 <= rating_value <= 5:
            return False, "Rating must be between 1 and 5"
            
        book = Book.query.get(book_isbn10)
        if not book:
            return False, "Book not found"
            
        existing_rating = Rating.query.filter_by(
            book_isbn10=book_isbn10,
            user_id=user_id
        ).first()
        
        if existing_rating:
            # Update existing rating
            old_rating = existing_rating.rating
            existing_rating.rating = rating_value
            
            # Update book's average rating
            total_rating = (book.Average_Rating * book.Number_of_Ratings - old_rating + rating_value)
            book.Average_Rating = total_rating / book.Number_of_Ratings
        else:
            # Add new rating
            new_rating = Rating(
                book_isbn10=book_isbn10,
                user_id=user_id,
                rating=rating_value
            )
            db.session.add(new_rating)
            
            # Update book's rating stats
            total_rating = (book.Average_Rating * book.Number_of_Ratings + rating_value)
            book.Number_of_Ratings += 1
            book.Average_Rating = total_rating / book.Number_of_Ratings
        
        db.session.commit()
        return True, "Rating successfully submitted"
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)

def get_user_rating(book_isbn10, user_id):
    """
    Get a user's rating for a specific book.
    
    Args:
        book_isbn10 (str): The book's ISBN10
        user_id (int): The user's ID
        
    Returns:
        int|None: The user's rating or None if not rated
    """
    rating = Rating.query.filter_by(
        book_isbn10=book_isbn10,
        user_id=user_id
    ).first()
    
    return rating.rating if rating else None
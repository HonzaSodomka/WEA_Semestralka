# rating.py
from . import db
from datetime import datetime

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_isbn10 = db.Column(db.String(10), db.ForeignKey('book.ISBN10'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure each user can only rate a book once
    __table_args__ = (db.UniqueConstraint('book_isbn10', 'user_id', name='unique_user_book_rating'),)
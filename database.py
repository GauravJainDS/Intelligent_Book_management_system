from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.Model):
    """
    Represents the 'books' table in the database.

    Attributes:
        id (int): The unique identifier for each book (primary key).
        title (str): The title of the book (non-nullable).
        author (str): The author of the book (non-nullable).
        genre (str): The genre of the book (optional).
        year_published (int): The year the book was published (optional).
        summary (str): A summary of the book (optional).

    This model maps to the 'books' table and stores information about books in the library.
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100))
    year_published = db.Column(db.Integer)
    summary = db.Column(db.Text)

class Reviews(db.Model):
    """
    Represents the 'reviews' table in the database.

    Attributes:
        id (int): The unique identifier for each review (primary key).
        book_id (int): The identifier of the book being reviewed (foreign key).
        user_id (int): The identifier of the user who wrote the review.
        review_text (str): The text of the review (optional).
        rating (int): The rating given by the user (optional).

    This model maps to the 'reviews' table and stores user reviews and ratings for books.
    """
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer)

def init_db(app):
    """
    Initialize the database with the given Flask application.

    Args:
        app (Flask): The Flask application instance to initialize the database for.

    This function initializes the SQLAlchemy database and creates all tables defined by the models.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()

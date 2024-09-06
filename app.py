from quart import Quart, request, jsonify
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from database import Books, Reviews  # Ensure these models are defined correctly
from Llama3.summary_generation import TextSummarizer
from recommendations.inference import BookRecommender
from config import Config

app = Quart(__name__)
app.config.from_object(Config)

# Initialize model paths and configuration
token = "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"
model_file_name = "meta-llama/Meta-Llama-3-8B"
model_path_recommendation = 'recommendations//Model//book_recommendation_knn_new1.pkl'
encoder_path = 'recommendations//Model//label_encoder_knn_new1.pkl'
y_train_path = 'recommendations//Model/y_train_knn_new1.pkl'

# Create async engine and session
DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/postgres"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_database():
    """
    Initializes the database connection. This function is called during the startup phase.

    It does not perform any operations on the database at the moment.
    """
    async with AsyncSessionLocal() as session:
        pass

@app.before_serving
async def startup():
    """
    Called before the Quart app starts serving. Initializes the database connection.

    This function ensures that the database is ready before the application starts accepting requests.
    """
    await init_database()
    async with app.app_context():
        pass

@app.route('/books', methods=['POST'])
async def add_book():
    """
    Adds a new book to the database.

    Expects JSON data with the book's title, author, genre, year published, and summary. 
    If the book already exists, returns an error. Otherwise, adds the book and returns its ID.

    Returns:
        JSON response with the ID of the newly added book or an error message if the book already exists.
    """
    data = await request.get_json()
    async with AsyncSessionLocal() as session:
        existing_book = await session.execute(
            select(Books).filter_by(title=data['title'], author=data['author'])
        )
        existing_book = existing_book.scalars().first()
        
        if existing_book:
            return jsonify({'error': 'Book already exists'}), 400

        new_book = Books(
            title=data['title'],
            author=data['author'],
            genre=data.get('genre'),
            year_published=data.get('year_published'),
            summary=data['summary']
        )
        session.add(new_book)
        await session.commit()
        return jsonify({'id': new_book.id}), 201

@app.route('/books', methods=['GET'])
async def get_books():
    """
    Retrieves all books from the database.

    Returns:
        JSON response with a list of all books, including their ID, title, and author.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Books))
        books = result.scalars().all()
        return jsonify([{'id': book.id, 'title': book.title, 'author': book.author} for book in books])

@app.route('/books/<int:book_id>', methods=['GET'])
async def get_book(book_id):
    """
    Retrieves a single book by its ID.

    Args:
        book_id (int): The ID of the book to retrieve.

    Returns:
        JSON response with the book's details or an error message if the book is not found.
    """
    async with AsyncSessionLocal() as session:
        book = await session.get(Books, book_id)
        if book is None:
            return jsonify({'error': 'Book not found'}), 404
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'year_published': book.year_published,
            'summary': book.summary
        })

@app.route('/books/<int:book_id>', methods=['PUT'])
async def update_book(book_id):
    """
    Updates the details of an existing book.

    Args:
        book_id (int): The ID of the book to update.

    Expects JSON data with the book's title, author, genre, year published, and summary. 
    If the book is not found, returns an error. Otherwise, updates the book and returns a success message.

    Returns:
        JSON response with a success message or an error message if the book is not found.
    """
    data = await request.get_json()

    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Retrieve the existing book record
            book = await session.get(Books, book_id)
            
            if book is None:
                return jsonify({'error': 'Book not found'}), 404

            # Update the book fields
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            book.genre = data.get('genre', book.genre)
            book.year_published = data.get('year_published', book.year_published)
            
            # Update summary if necessary
            book.summary = data.get('summary', book.summary)  #await Llama3Model.generate_summary(data.get('summary', book.summary))

            # Commit the changes
            await session.commit()
            
            return jsonify({'message': 'Book updated successfully'}), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
async def delete_book(book_id):
    """
    Deletes a book from the database.

    Args:
        book_id (int): The ID of the book to delete.

    Returns:
        JSON response with a success message or an error message if the book is not found.
    """
    async with AsyncSessionLocal() as session:
        book = await session.get(Books, book_id)
        if book is None:
            return jsonify({'error': 'Book not found'}), 404
        await session.delete(book)
        await session.commit()
        return jsonify({'message': 'Book deleted successfully'})

@app.route('/books/<int:book_id>/reviews', methods=['POST'])
async def add_review(book_id):
    """
    Adds a review for a book.

    Args:
        book_id (int): The ID of the book to review.

    Expects JSON data with the user ID, review text, and rating. Adds the review to the database and returns its ID.

    Returns:
        JSON response with the ID of the newly added review.
    """
    data = await request.get_json()
    async with AsyncSessionLocal() as session:
        new_review = Reviews(
            book_id=book_id,
            user_id=data['user_id'],
            review_text=data['review_text'],
            rating=data['rating']
        )
        session.add(new_review)
        await session.commit()
        return jsonify({'id': new_review.id}), 201

@app.route('/books/<int:book_id>/reviews', methods=['GET'])
async def get_reviews(book_id):
    """
    Retrieves all reviews for a specific book.

    Args:
        book_id (int): The ID of the book for which to retrieve reviews.

    Returns:
        JSON response with a list of reviews for the specified book.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Reviews).filter_by(book_id=book_id))
        reviews = result.scalars().all()
        return jsonify([{'id': review.id, 'review_text': review.review_text, 'rating': review.rating} for review in reviews])

@app.route('/textsummarizer', methods=['GET'])
async def get_book_summary():
    """
    Generates a summary for the provided book content.

    Expects a query parameter `book_content` containing the text to summarize. Uses the `TextSummarizer` to generate a summary.

    Returns:
        JSON response with the generated summary.
    """
    book_content = request.args.get('book_content')
    summarizer = TextSummarizer(token, model_path=model_file_name)
    summary = summarizer.extract_summary(book_content) 
    return jsonify({'summary': summary})

@app.route('/recommendations', methods=['GET'])
async def get_recommendations():
    """
    Provides book recommendations based on genre and rating threshold.

    Expects query parameters `genre` and `rating` to filter recommendations. Uses the `BookRecommender` to generate a list of recommended books.

    Returns:
        JSON response with a list of recommended books.
    """
    recommender = BookRecommender(model_path=model_path_recommendation, encoder_path=encoder_path, y_train_path=y_train_path)
    genre = request.args.get('genre')
    rating_threshold = request.args.get('rating', type=int)
    recommended_books = recommender.recommend_books(genre, rating_threshold)
    return jsonify({'Recommended books for you': recommended_books})

if __name__ == '__main__':
    app.run(debug=True)

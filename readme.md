# Intelligent Book Management System

## Overview

This project is an intelligent book management system built using Python, a locally running Llama3 generative AI model. The system provides functionalities to add, retrieve, update, and delete books from a PostgreSQL database. It also generates summaries for books using the Llama3 model, offers book recommendations based on user preferences, and manages user reviews with rating and review summaries. The system is accessible via a RESTful API.

## Components

The project consists of the following parts:

1. **Llama3 Text Summarization**: Code for generating summaries of book content using the Llama3 model.
2. **Book Recommendations**: Code for providing book recommendations based on genre and average rating using a KNN model.
3. **Application**: The main Quart application that exposes the RESTful API endpoints.
4. **Configuration**: Configuration settings for the database.
5. **Database**: Database initialization code.
6. **Request Examples**: Sample code for interacting with the API.

## Directory Structure
```
/intelligent-book-management
    ├── /Llama3
    │   └── summarization.py
    |   |__ token key for model access
    |
    ├── /recommendations
    │   └── inference.py
    |   |__ models for recommendations
    ├── app.py
    ├── config.py
    ├── database.py
    ├── requirements.txt
    └── request_examples.py

### Llama3 Text Summarization

**File:** `Llama3/summarization.py`

This module contains the `TextSummarizer` class, which uses the Llama3 model to generate and extract summaries from book content.

### Book Recommendations

**File:** `recommendations/inference.py`

This module contains the `BookRecommender` class, which provides book recommendations based on genre and average rating using a KNN model.

### Application

**File:** `app.py`

The main Quart application file that sets up the RESTful API endpoints for managing books, reviews, and generating summaries.

### Configuration

**File:** `config.py`

Contains configuration settings for the application, including the database URL.

### Database

**File:** `database.py`

Defines tables for `Books` and `Reviews` and provides initialization functions.

### Request Examples

**File:** `request_examples.py`

Contains sample code demonstrating how to interact with the API endpoints and see functions of book mangement system.

## Setup and Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/intelligent-book-management.git
    cd intelligent-book-management
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```
4. Download Postgress and creates two table books and reviews by Scrript

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,          -- Unique identifier for each book
    title VARCHAR(150) NOT NULL,    -- Title of the book
    author VARCHAR(100) NOT NULL,   -- Author of the book
    genre VARCHAR(50),              -- Genre of the book
    year_published INT,             -- Year the book was published
    summary TEXT                    -- Summary of the book
);


--CREATE TABLE IF NOT EXISTS reviews (
--    id SERIAL PRIMARY KEY,          -- Unique identifier for each review
--    book_id INT REFERENCES books(id) ON DELETE CASCADE,  -- Foreign key referencing the books table
--    user_id INT NOT NULL,           -- Identifier for the user who wrote the review
--    review_text TEXT,               -- Text of the review
--    rating INT CHECK (rating >= 1 AND rating <= 5)  -- Rating between 1 and 5
--);
```

4. **Configure Environment Variables**

    Create a `.env` file in the root directory and add the following variables:

    ```
    DATABASE_URL=postgresql://postgres:admin@localhost/postgres
    ```

5. **Initialize the Database**

    Ensure your PostgreSQL server is running and execute the database setup:

    ```python
    from app import init_database
    import asyncio

    asyncio.run(init_database())
    ```

6. **Run the Application**

    ```bash
    python app.py
    ```

## API Endpoints

- **Add a Book**

    - **Endpoint:** `POST /books`
    - **Request Body:**
      ```json
      {
        "title": "Book Title",
        "author": "Author Name",
        "genre": "Genre",
        "year_published": 2020,
        "summary": "Book summary."
      }
      ```

- **Retrieve All Books**

    - **Endpoint:** `GET /books`

- **Retrieve a Specific Book**

    - **Endpoint:** `GET /books/<int:book_id>`

- **Update a Book**

    - **Endpoint:** `PUT /books/<int:book_id>`
    - **Request Body:**
      ```json
      {
        "title": "Updated Title",
        "author": "Updated Author",
        "genre": "Updated Genre",
        "year_published": 2021,
        "summary": "Updated summary."
      }
      ```

- **Delete a Book**

    - **Endpoint:** `DELETE /books/<int:book_id>`

- **Add a Review**

    - **Endpoint:** `POST /books/<int:book_id>/reviews`
    - **Request Body:**
      ```json
      {
        "user_id": 1,
        "review_text": "Review text.",
        "rating": 4
      }
      ```

- **Retrieve Reviews for a Book**

    - **Endpoint:** `GET /books/<int:book_id>/reviews`

- **Generate Book Summary**

    - **Endpoint:** `GET /textsummarizer`
    - **Query Parameters:**
      - `book_content`: The content of the book to summarize.

- **Get Book Recommendations**

    - **Endpoint:** `GET /recommendations`
    - **Query Parameters:**
      - `genre`: Genre of books to recommend.
      - `rating`: Minimum average rating.

## Testing

Use the provided `request_examples.py` file to test the API endpoints. Modify the code as needed to suit your local setup and test various functionalities.


## Requirements

- Python 3.11
- Quart
- SQLAlchemy
- PostgreSQL
- PyTorch
- Transformers
- LangChain

Install the dependencies listed in `requirements.txt` to ensure compatibility.



## Acknowledgements

- [Llama3 Model](https://huggingface.co/Meta/llama-3-8b)
- [PostgreSQL](https://www.postgresql.org/)


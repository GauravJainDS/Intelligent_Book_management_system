import requests
import urllib.parse

### Add a Book
# Sends a POST request to add a new book to the database.
# 
# URL: http://127.0.0.1:5000/books
# Data payload:
# {
#     "title": "Descent of the suns1",
#     "author": "Korean author1",
#     "genre": "Love1",
#     "year_published": 2019,
#     "summary": "Series of a doctor and military man1."
# }
#
# Response:
# Prints the HTTP status code and JSON response from the server.
url = "http://127.0.0.1:5000/books"
data = {
    "title": "Descent of the suns1",
    "author": "Korean author1",
    "genre": "Love1",
    "year_published": 2019,
    "summary": "Series of a doctor and military man1."
}
response = requests.post(url, json=data)
print("Add Book:", response.status_code, response.json())


### Get All Books Details
# Sends a GET request to retrieve all book details from the database.
# 
# URL: http://127.0.0.1:5000/books
# Response:
# Prints the HTTP status code and JSON response containing all books.
url = "http://127.0.0.1:5000/books"
response = requests.get(url)
print("Get All Books:", response.status_code, response.json())


### Get a Specific Book
# Sends a GET request to retrieve details of a specific book by its ID.
# 
# URL: http://127.0.0.1:5000/books/{book_id}
# Replace {book_id} with the actual book ID (e.g., 4).
# Response:
# Prints the HTTP status code and JSON response containing the book details.
book_id = 4
url = f"http://127.0.0.1:5000/books/{book_id}"
response = requests.get(url)
print("Get Book:", response.status_code, response.json())


### Update Book Content
# Sends a PUT request to update the details of a specific book by its ID.
# 
# URL: http://127.0.0.1:5000/books/{book_id}
# Replace {book_id} with the actual book ID (e.g., 4).
# Data payload:
# {
#     "title": "The Great Gatsby (Updated1)",
#     "author": "F. Scott Fitzgerald (Updated1)",
#     "genre": "Classic Fiction",
#     "year_published": 1995,
#     "summary": "An updated summary of the novel1."
# }
# Response:
# Prints the HTTP status code and JSON response confirming the update.
book_id = 4
url = f"http://127.0.0.1:5000/books/{book_id}"
data = {
    "title": "The Great Gatsby (Updated1)",
    "author": "F. Scott Fitzgerald (Updated1)",
    "genre": "Classic Fiction",
    "year_published": 1995,
    "summary": "An updated summary of the novel1."
}
response = requests.put(url, json=data)
print("Update Book:", response.status_code, response.json())


### Delete a Book
# Sends a DELETE request to remove a specific book from the database by its ID.
# 
# URL: http://127.0.0.1:5000/books/{book_id}
# Replace {book_id} with the actual book ID (e.g., 3).
# Response:
# Prints the HTTP status code and JSON response confirming the deletion.
book_id = 3
url = f"http://127.0.0.1:5000/books/{book_id}"
response = requests.delete(url)
print("Delete Book:", response.status_code, response.json())


### Add a Summary
# Sends a GET request to generate a summary of the given book content.
# 
# URL: http://127.0.0.1:5000/textsummarizer
# Data payload:
# book_content = """
# Maria Sharapova has basically no friends as tennis players on the WTA Tour...
# """
# Response:
# Prints the raw content and JSON response with the generated summary.
url = "http://127.0.0.1:5000/textsummarizer"
book_content = """
Maria Sharapova has basically no friends as tennis players on the WTA Tour...
"""
encoded_book_content = urllib.parse.quote(book_content)
full_url = f"{url}?book_content={encoded_book_content}"
response = requests.get(full_url)
print("Raw Response Content:", response.content)
try:
    print("Get Summary:", response.status_code, response.json())
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON response.")


### Check Recommendations
# Sends a GET request to retrieve book recommendations based on genre and rating.
# 
# URL: http://127.0.0.1:5000/recommendations?genre=Fiction&rating=4
# Response:
# Prints the HTTP status code and JSON response containing the recommended books.
url = "http://127.0.0.1:5000/recommendations?genre=Fiction&rating=4"
response = requests.get(url)
print("Get Recommendations:", response.status_code, response.json())


### Add a Review
# Sends a POST request to add a review for a specific book by its ID.
# 
# URL: http://127.0.0.1:5000/books/{book_id}/reviews
# Replace {book_id} with the actual book ID (e.g., 5).
# Data payload:
# {
#     "user_id": 12311,
#     "review_text": "Awesome!",
#     "rating": 4.8
# }
# Response:
# Prints the HTTP status code and JSON response with the added review details.
book_id = 5
url = f"http://127.0.0.1:5000/books/{book_id}/reviews"
data = {
    "user_id": 12311,
    "review_text": "Awesome!",
    "rating": 4.8
}
response = requests.post(url, json=data)
print("Add Review:", response.status_code, response.json())

### Get Reviews for a Book
# Sends a GET request to retrieve all reviews for a specific book by its ID.
# 
# URL: http://127.0.0.1:5000/books/{book_id}/reviews
# Replace {book_id} with the actual book ID (e.g., 5).
# Response:
# Prints the HTTP status code and JSON response containing the reviews for the book.
book_id = 5
url = f"http://127.0.0.1:5000/books/{book_id}/reviews"
response = requests.get(url)
print("Get Reviews:", response.status_code, response.json())

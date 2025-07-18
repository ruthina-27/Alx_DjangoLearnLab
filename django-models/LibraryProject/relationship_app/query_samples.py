from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author.
def query_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    print("Books by author:", [book.title for book in books])

# List all books in a library.
def list_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    print("Books in library:", [book.title for book in books])

# Retrieve the librarian for a library.
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = library.librarian
    print("Librarian for library:", librarian.name)

# Example usage (uncomment and adjust names as needed):
# query_books_by_author("Some Author")
# list_books_in_library("Some Library")
# get_librarian_for_library("Some Library") 
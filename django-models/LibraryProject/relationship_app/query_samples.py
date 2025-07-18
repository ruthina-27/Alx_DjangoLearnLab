from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
specific_author = Author.objects.get(name="Some Author")
authors_books = Book.objects.filter(author=specific_author)
print("Books by", specific_author.name, ":", list(authors_books))

# List all books in a library
library = Library.objects.get(name="Some Library")
library_books = library.books.all()
print("Books in", library.name, ":", list(library_books))

# Retrieve the librarian for a library
librarian = library.librarian  # OneToOneField reverse access
print("Librarian for", library.name, ":", librarian.name) 
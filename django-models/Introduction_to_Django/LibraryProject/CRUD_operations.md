# CRUD Operations for Book Model

## Create
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```
**Expected Output:**
```
1984 by George Orwell (1949)
```

## Retrieve
```python
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
```
**Expected Output:**
```
1984 George Orwell 1949
```

## Update
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
```
**Expected Output:**
```
Nineteen Eighty-Four
```

## Delete
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(Book.objects.all())
```
**Expected Output:**
```
<QuerySet []>
``` 
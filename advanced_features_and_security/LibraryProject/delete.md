# Delete Book Instance

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(Book.objects.all())
```

# Expected Output
```
<QuerySet []>
``` 
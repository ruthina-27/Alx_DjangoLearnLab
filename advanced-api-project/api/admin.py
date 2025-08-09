from django.contrib import admin
from .models import Author, Book

# Register the Author model to manage authors in the admin interface.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Register the Book model to manage books in the admin interface.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publication_year', 'author')
    list_filter = ('publication_year', 'author')
    search_fields = ('title',)

# This setup allows you to easily create, view, and manage Author and Book instances
# through the Django admin panel, which is useful for manual testing and data entry.

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm
from .forms import ExampleForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

# Create your views here.

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    response = render(request, 'bookshelf/book_list.html', {'books': books})
    # Set a basic CSP header to mitigate XSS
    response["Content-Security-Policy"] = "default-src 'self'"
    return response

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Documentation: Permissions and Groups
# -------------------------------------
# Custom permissions (can_view, can_create, can_edit, can_delete) are defined in Book's Meta class.
# Use Django admin to create groups (Editors, Viewers, Admins) and assign these permissions to each group:
#   - Editors: can_create, can_edit, can_view
#   - Viewers: can_view
#   - Admins: can_create, can_edit, can_delete, can_view
# Assign users to groups via the admin interface.
# The @permission_required decorator enforces these permissions in views.

# CSP header is set in book_list view to reduce XSS risk. Adjust as needed for your static/media domains.

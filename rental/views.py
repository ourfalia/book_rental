from django.shortcuts import render, get_object_or_404
from .models import Book
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'rental/book_list.html', {'books': books})
    

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'rental/book_detail.html', {'book': book})
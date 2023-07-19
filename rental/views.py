from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'rental/book_list.html', {'books': books})
    
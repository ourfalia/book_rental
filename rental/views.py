from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Reservation
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.


@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'rental/book_list.html', {'books': books})
    

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'rental/book_detail.html', {'book': book})

@login_required
def reserve_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        user = request.user

        if Reservation.objects.filter(book=book, start_date__lte=end_date, end_date__gte=start_date).exists():
            return render(request, 'rental/book_unavailable.html', {'book': book})

        reservation = Reservation.objects.create(book=book, user=user, start_date=start_date, end_date=end_date)
        return redirect('book_detail', pk=book.pk)

    return render(request, 'rental/book_reserve.html', {'book': book})


@login_required
def add_to_bag(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user = request.user

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        cart_item, created = CartItem.objects.get_or_create(user=user, book=book)
        cart_item.quantity += quantity
        cart_item.save()
        return redirect('view_bag')

    return render(request, 'rental/add_to_bag.html', {'book': book})


@login_required
def view_bag(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = cart_items.aggregate(total=Sum('book__price'))['total'] or 0
    return render(request, 'rental/view_bag.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user, is_checked_out=False)
    total_price = 0

    for reservation in reservations:
        num_days = (reservation.end_date - reservation.start_date).days + 1
        reservation.price = num_days * 2  
        total_price += reservation.price

    if request.method == 'POST':
        for reservation in reservations:
            reservation.is_checked_out = True
            reservation.save()

        return redirect('checkout_success')

    return render(request, 'rental/checkout.html', {'reservations': reservations, 'total_price': total_price})

@login_required
def checkout_success(request):
    return render(request, 'rental/checkout_success.html')
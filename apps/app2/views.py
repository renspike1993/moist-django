from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from datetime import timedelta
from django.utils import timezone

from apps.app1.models import Student
from .models import Book,BorrowedBook,BookBarcode
from .forms import BookForm
from django.contrib import messages
from django.db.models import Prefetch


@login_required
def index(request):
    return render(request, 'app2/index.html')
@login_required
def opac(request):
    return render(request, 'app2/opac.html')


# List all books
@login_required
def book_list(request):
    return render(request, 'app2/book/book_list.html', {'books': Book.objects.all() })


# View book details
@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "app2/book/book_detail.html", {"book": book})

# Create a new book
@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'app2/book/book_form.html', {'form': form})

# Update an existing book
@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'app2/book/book_form.html', {'form': form})

# Delete a book
@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'app2/book/book_confirm_delete.html', {'book': book})


@login_required
def borrow_book_list(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    books = Book.objects.prefetch_related("barcodes").all()

    # Prepare a set of borrowed barcode IDs
    borrowed_barcodes = set(
        BorrowedBook.objects.filter(borrower=student, status="borrowed")
        .values_list("barcode_id", flat=True)
    )

    context = {
        "student": student,
        "books": books,
        "borrowed_barcodes": borrowed_barcodes,
    }
    return render(request, "app2/book/borrow_book_list.html", context)


@login_required
def borrow_book(request, student_id, book_id, barcode_id):
    student = get_object_or_404(Student, pk=student_id)
    book = get_object_or_404(Book, pk=book_id)
    barcode = get_object_or_404(BookBarcode, pk=barcode_id)

    # Create BorrowedBook record
    BorrowedBook.objects.create(
        borrower=student,
        book=book,
        barcode=barcode,
        due_date=timezone.now().date() + timedelta(days=7)  # 7-day borrowing period
    )

    messages.success(request, f"{book.title} ({barcode.barcode}) borrowed successfully!")
    return redirect('borrow_book_list', student_id=student.id)

@login_required
def bookbarcode_create(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        barcode_value = request.POST.get("barcode")

        if not barcode_value:
            messages.error(request, "Barcode is required.")
            return redirect("bookbarcode_create", pk=pk)

        # Prevent duplicate barcode
        if BookBarcode.objects.filter(barcode=barcode_value).exists():
            messages.error(request, "This barcode already exists!")
            return redirect("bookbarcode_create", pk=pk)

        BookBarcode.objects.create(book=book, barcode=barcode_value)
        messages.success(request, "Barcode added successfully!")
        return redirect("book_detail", pk=pk)

    return render(request, "app2/book/bookbarcode_form.html", {"book": book})


@login_required
def return_book(request, borrowed_id):
    borrowed = get_object_or_404(BorrowedBook, pk=borrowed_id)

    if borrowed.status == 'borrowed':
        borrowed.status = 'returned'
        borrowed.date_returned = timezone.now()
        borrowed.save()
        messages.success(request, f"{borrowed.book.title} has been returned successfully.")
    else:
        messages.warning(request, f"{borrowed.book.title} was already returned.")

    return redirect('student_detail', pk=borrowed.borrower.id)
# ----------------------------------------------------------------------------------


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from datetime import timedelta
from django.utils import timezone

from apps.app1.models import Student
from .models import Book,BorrowedBook
from .forms import BookForm
from django.contrib import messages


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
    return render(request, 'app2/book/book_detail.html', {'book': book})

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
    student = Student.objects.get(pk=student_id)
    books = Book.objects.all()

    borrowed_books = BorrowedBook.objects.filter(borrower=student)

    return render(request, "app2/book/borrow_book_list.html", {
        "student": student,
        "books": books,
        "borrowed_books": borrowed_books,
    })

def borrow_book(request, student_id, book_id):
    student = get_object_or_404(Student, pk=student_id)
    book = get_object_or_404(Book, pk=book_id)

    BorrowedBook.objects.create(
        borrower=student,
        book=book,
        due_date=timezone.now().date() + timedelta(days=7)
    )

    messages.success(request, f"{book.title} borrowed successfully!")
    return redirect('borrow_book_list', student_id=student_id)

# ----------------------------------------------------------------------------------


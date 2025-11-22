from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from datetime import timedelta
from django.utils import timezone

from apps.app1.models import Student
from .models import Book,BorrowedBook,BookBarcode,Collection
from .forms import BookForm,CollectionForm
from django.contrib import messages
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q,Count
from django.http import JsonResponse

def ads(request):
    return render(request, 'app2/tv.html')










@login_required
def dashboard(request):
    # Total counts
    total_books = Book.objects.count()
    total_barcodes = BookBarcode.objects.count()
    total_collections = Collection.objects.count()
    total_students = Student.objects.count()

    # Borrowed stats
    borrowed_count = BorrowedBook.objects.filter(status="borrowed").count()
    returned_count = BorrowedBook.objects.filter(status="returned").count()
    overdue_count = BorrowedBook.objects.filter(status="overdue").count()

    # Recently added books
    recent_books = Book.objects.order_by('-created_at')[:5]

    # Recently borrowed books
    recent_borrowed = BorrowedBook.objects.select_related('book', 'borrower', 'barcode').order_by('-date_borrowed')[:5]

    context = {
        'total_books': total_books,
        'total_barcodes': total_barcodes,
        'total_collections': total_collections,
        'total_students': total_students,
        'borrowed_count': borrowed_count,
        'returned_count': returned_count,
        'overdue_count': overdue_count,
        'recent_books': recent_books,
        'recent_borrowed': recent_borrowed,
    }

    return render(request, 'app2/dashboard.html', context)



@login_required
def index(request):
    return render(request, 'app2/index.html')

@login_required
def opac(request):
    books_list = Book.objects.all()
    paginator = Paginator(books_list, 10)  # 10 books per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app2/opac.html', {'books': page_obj, 'page_obj': page_obj})


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

    # Search query
    q = request.GET.get("q", "").strip().upper()

    # Step 1: Get all barcodes that are currently borrowed
    borrowed_barcodes = BorrowedBook.objects.filter(status="borrowed").values_list("barcode_id", flat=True)

    # Step 2: Get books with at least one available barcode
    books = Book.objects.prefetch_related("barcodes").filter(
        barcodes__id__isnull=False  # Make sure book has barcodes
    ).exclude(
        barcodes__id__in=borrowed_barcodes  # Exclude borrowed barcodes
    ).distinct()

    # Step 3: Filter by search query if provided
    if q:
        books = books.filter(barcodes__barcode__iexact=q).distinct()

    # Pagination
    paginator = Paginator(books, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Prepare a set of borrowed barcodes for this student (optional, for UI purposes)
    student_borrowed_barcodes = set(
        BorrowedBook.objects.filter(
            borrower=student,
            status="borrowed"
        ).values_list("barcode_id", flat=True)
    )

    context = {
        "student": student,
        "page_obj": page_obj,
        "borrowed_barcodes": student_borrowed_barcodes,
        "q": q,
    }
    return render(request, "app2/book/borrow_book_list.html", context)


@login_required
def all_books_borrow_history(request):
    status_filter = request.GET.get('status', '')  # 'borrowed', 'returned', 'overdue' or ''
    search_query = request.GET.get('q', '').strip()

    # Base queryset
    borrow_records = BorrowedBook.objects.select_related(
        'book', 'borrower', 'barcode'
    ).order_by('-date_borrowed')

    # Apply status filter if provided
    if status_filter in ['borrowed', 'returned', 'overdue']:
        borrow_records = borrow_records.filter(status=status_filter)

    # Apply search filter if provided
    if search_query:
        borrow_records = borrow_records.filter(
            Q(book__title__icontains=search_query) |
            Q(book__author__icontains=search_query) |
            Q(barcode__barcode__icontains=search_query) |
            Q(borrower__first_name__icontains=search_query) |
            Q(borrower__last_name__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(borrow_records, 10)  # 15 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'borrow_records': page_obj,
        'status_filter': status_filter,
        'q': search_query,
        'page_obj': page_obj,
    }
    return render(request, 'app2/book/all_books_borrow_history.html', context)


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
        due_date=timezone.now().date() + timedelta(days=3)  # 7-day borrowing period
    )

    messages.success(request, f"{book.title} ({barcode.barcode}) borrowed successfully!")
    return redirect('borrow_book_list', student_id=student.id)


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

    # Redirect back to the previous page, fallback to home if not available
    return redirect(request.META.get('HTTP_REFERER', '/'))

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
def bookbarcode_delete(request, book_id, barcode_id):
    # Get the book and barcode (404 if not found)
    book = get_object_or_404(Book, pk=book_id)
    barcode = get_object_or_404(BookBarcode, pk=barcode_id, book=book)

    # Delete the barcode
    barcode.delete()
    messages.success(request, f"Barcode {barcode.barcode} was deleted successfully.")

    # Return to book detail page
    return redirect("book_detail", pk=book_id)
# ----------------------------------------------------------------------------------

@login_required
def security_logs(request):
    return render(request, 'app2/logs.html')


# -------------------------------

@login_required
def all_borrowed_books(request):
    q = request.GET.get("q", "").strip()

    borrowed = BorrowedBook.objects.select_related("borrower", "book", "barcode")

    if q:
        borrowed = borrowed.filter(
            Q(book__title__icontains=q) |
            Q(book__author__icontains=q) |
            Q(barcode__barcode__icontains=q) |
            Q(borrower__first_name__icontains=q) |
            Q(borrower__last_name__icontains=q)
        )

    paginator = Paginator(borrowed.order_by("-date_borrowed"), 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "q": q}
    return render(request, "app2/book/borrowed_all_list.html", context)



@login_required
def api_check_book_status(request, barcode):
    try:
        # Get the barcode object and related book
        barcode_obj = BookBarcode.objects.select_related("book").get(barcode=barcode)

        # Check if this copy is currently borrowed (date_returned is None)
        borrowed = BorrowedBook.objects.select_related("borrower").filter(
            barcode=barcode_obj,
            date_returned__isnull=True  # only still borrowed
        ).first()

        if borrowed:
            return JsonResponse({
                "status": "borrowed",
                "book_title": barcode_obj.book.title,
                "borrower": f"{borrowed.borrower.first_name} {borrowed.borrower.last_name}",
                "date_borrowed": borrowed.date_borrowed.strftime("%Y-%m-%d %H:%M"),
            })

        # If not borrowed, the book is available
        return JsonResponse({
            "status": "available",
            "book_title": barcode_obj.book.title,
        })

    except BookBarcode.DoesNotExist:
        # Barcode does not exist
        return JsonResponse({"status": "not_found"})
    

# -------------------------------Collection------------------------------------------------

# LIST COLLECTIONS WITH BOOK COUNT
def collection_list(request):
    collections = Collection.objects.annotate(
        book_count=Count('books')  # 'books' is the related_name from Book.collection
    ).order_by('-id')
    
    return render(request, 'app2/collection/collection_list.html', {'collections': collections})

# CREATE COLLECTION
def collection_create(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('collection_list')
    else:
        form = CollectionForm()
    return render(request, 'app2/collection/collection_form.html', {'form': form})

# UPDATE COLLECTION
def collection_update(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return redirect('collection_list')
    else:
        form = CollectionForm(instance=collection)
    return render(request, 'app2/collection/collection_form.html', {'form': form})

# DELETE COLLECTION
def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'POST':
        collection.delete()
        return redirect('collection_list')
    return render(request, 'app2/collection/collection_confirm_delete.html', {'collection': collection})

# VIEW COLLECTION DETAILS
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    return render(request, 'app2/collection/collection_detail.html', {'collection': collection})
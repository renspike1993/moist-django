# apps.app3/models.py
from django.db import models
from apps.app1.models import Student   # adjust path if needed
from django.utils import timezone


class Book(models.Model):
    # Control number / unique ID
    control_number = models.CharField(max_length=50, unique=True, verbose_name="Control Number / 001")
    
    # ISBN
    isbn = models.CharField(max_length=20, blank=True, null=True, verbose_name="ISBN / 020")
    
    # Title statement
    title = models.CharField(max_length=255, verbose_name="Title / 245$a")
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subtitle / 245$b")
    statement_of_responsibility = models.CharField(max_length=255, blank=True, null=True, verbose_name="Statement of Responsibility / 245$c")
    
    # Author
    author = models.CharField(max_length=255, verbose_name="Main Author / 100$a")
    added_authors = models.CharField(max_length=255, blank=True, null=True, verbose_name="Added Authors / 700$a")
    
    # Edition
    edition = models.CharField(max_length=100, blank=True, null=True, verbose_name="Edition / 250")
    
    # Publication info
    publisher = models.CharField(max_length=255, blank=True, null=True, verbose_name="Publisher / 264$b")
    publication_place = models.CharField(max_length=255, blank=True, null=True, verbose_name="Place / 264$a")
    publication_year = models.CharField(max_length=4, blank=True, null=True, verbose_name="Year / 264$c")
    
    # Physical description
    pages = models.CharField(max_length=50, blank=True, null=True, verbose_name="Pagination / 300$a")
    illustrations = models.CharField(max_length=255, blank=True, null=True, verbose_name="Illustrations / 300$b")
    dimensions = models.CharField(max_length=50, blank=True, null=True, verbose_name="Dimensions / 300$c")
    
    # Series info
    series = models.CharField(max_length=255, blank=True, null=True, verbose_name="Series / 490$a")
    
    # Notes and summary
    notes = models.TextField(blank=True, null=True, verbose_name="General Notes / 500")
    summary = models.TextField(blank=True, null=True, verbose_name="Summary / 520")
    
    # Subjects
    subjects = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subjects / 650$a")
    
    # Classification / Call number
    classification = models.CharField(max_length=50, blank=True, null=True, verbose_name="Dewey / 082 or Local / 090")
    
    # Language
    language = models.CharField(max_length=50, blank=True, null=True, verbose_name="Language / 041$a")
    
    # Created / updated timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

class BookBarcode(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name="barcodes")
    barcode = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.barcode} - {self.book.title}"

class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")
    borrower = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="borrowed_books")
        
    date_borrowed = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    date_returned = models.DateField(blank=True, null=True)

    remarks = models.CharField(max_length=255, blank=True, null=True)

    STATUS_CHOICES = [
        ("borrowed", "Borrowed"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="borrowed")

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower.first_name} {self.borrower.last_name}"




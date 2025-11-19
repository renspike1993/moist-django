# apps.app3/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'control_number': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Control Number / 001'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'ISBN / 020'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Title / 245$a'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Subtitle / 245$b'
            }),
            'statement_of_responsibility': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Statement of Responsibility / 245$c'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Main Author / 100$a'
            }),
            'added_authors': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Added Authors / 700$a'
            }),
            'edition': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Edition / 250'
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Publisher / 264$b'
            }),
            'publication_place': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Place / 264$a'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Year / 264$c',
                'min': 1000,
                'max': 9999
            }),
            'pages': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Pagination / 300$a'
            }),
            'illustrations': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Illustrations / 300$b'
            }),
            'dimensions': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Dimensions / 300$c'
            }),
            'series': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Series / 490$a'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'General Notes / 500',
                'rows': 3
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Summary / 520',
                'rows': 3
            }),
            'subjects': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Subjects / 650$a'
            }),
            'classification': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Dewey / 082 or Local / 090'
            }),
            'language': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Language / 041$a'
            }),
        }


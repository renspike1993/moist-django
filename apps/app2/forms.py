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
                'placeholder': 'Control Number'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'ISBN'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Title'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Subtitle'
            }),
            'statement_of_responsibility': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Statement of Responsibility'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Main Author'
            }),
            'added_authors': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Added Authors'
            }),
            'edition': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Edition'
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Publisher'
            }),
            'publication_place': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Place of Publication'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Year',
                'min': 1000,
                'max': 9999
            }),
            'pages': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Pages'
            }),
            'illustrations': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Illustrations'
            }),
            'dimensions': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Dimensions'
            }),
            'series': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Series'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'General Notes',
                'rows': 2
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Summary',
                'rows': 2
            }),
            'subjects': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Subjects'
            }),
            'classification': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Dewey / Local'
            }),
            'language': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Language'
            }),
        }

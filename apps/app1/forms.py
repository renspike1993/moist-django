from django import forms
from .models import Student,Folder

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        
        

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['folder_name', 'folder_capacity', 'floor_number']
        widgets = {
            'folder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'folder_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'floor_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import group_required  # use the decorator from decorators.py
from .forms import StudentForm
from .models import Student

# Home page
def home(request):
    return render(request, 'blog/home.html')

# Login view
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password"
    return render(request, 'blog/login.html', {'error': error})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Editor-only view
@login_required
@group_required('Editors')
def edit_blog(request):
    return HttpResponse("You can edit blogs!")

# Manager-only view
@login_required
@group_required('Managers')
def manage_users(request):
    return HttpResponse("You can manage users!")

# List all students with pagination
@login_required
@group_required('Editors')  # Only editors can view/manage students
def student_list(request):
    students = Student.objects.all().order_by('full_name')  # Order alphabetically
    paginator = Paginator(students, 10)  # Show 10 students per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Handles invalid page numbers automatically

    return render(request, 'student/student_list.html', {'page_obj': page_obj})


# Add student
@login_required
@group_required('Editors')
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student/student_form.html', {'form': form})

# Edit student
@login_required
@group_required('Editors')
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student/student_form.html', {'form': form, 'student': student})

# Delete student
@login_required
@group_required('Editors')
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'student/student_delete.html', {'student': student})

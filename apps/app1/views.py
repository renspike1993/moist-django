from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

from apps.app2.models import BorrowedBook


@login_required
def index(request):
    return render(request, 'app1/index.html')


# READ (LIST)
@login_required
def student_list(request):
    students = Student.objects.all().order_by("last_name")
    return render(request, "app1/student/student_list.html", {"students": students})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)

    borrowed_books = student.borrowed_books.select_related("book").all()

    return render(request, "app1/student/student_detail.html", {
        "student": student,
        "borrowed_books": borrowed_books,
    })

# CREATE
@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "app1/student/student_form.html", {"form": form, "title": "Add Student"})

# UPDATE
@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("app1/student_list")
    else:
        form = StudentForm(instance=student)
    return render(request, "app1/student/student_form.html", {"form": form, "title": "Edit Student"})

# DELETE
@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect("student_list")
    return render(request, "app1/student/student_confirm_delete.html", {"student": student})


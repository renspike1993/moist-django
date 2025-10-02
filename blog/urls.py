from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('edit-blog/', views.edit_blog, name='edit_blog'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
        
        
    # path('about/', views.about, name='about'),
]

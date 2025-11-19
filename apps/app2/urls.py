from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='library'),
    path('opac/', views.opac, name='opac'),
    path('list/', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('<int:pk>/edit/', views.book_update, name='book_update'),
    path('<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('borrow-books/<int:student_id>/', views.borrow_book_list, name='borrow_book_list'),
    path(
        'borrow-books/<int:student_id>/<int:book_id>/borrow/',
        views.borrow_book,
        name='borrow_book'
    ),    
    path("books/<int:pk>/barcode/add/", views.bookbarcode_create, name="bookbarcode_create"),

]

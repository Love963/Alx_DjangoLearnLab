from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    add_book,         
    edit_book,         
    delete_book,       
    register,
    admin_view,
    librarian_view,
    member_view,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Book views
    path('books/', list_books, name='list_books'),  # FBV
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # CBV

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),


    # Dashboards
    path('admin-dashboard/', admin_view, name='admin_view'),
    path('librarian-dashboard/', librarian_view, name='librarian_view'),
    path('member-dashboard/', member_view, name='member_view'),

    # Book CRUD
    path('books/add/', add_book, name='add_book'), 
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),  
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),  
]

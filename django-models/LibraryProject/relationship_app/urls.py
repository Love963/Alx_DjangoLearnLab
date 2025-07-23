from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    register_view,
    login_view,
    logout_view,
    home_view,
    admin_view,
    librarian_view,
    member_view,
)

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Auth views
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Role-based home views
    path('home/', home_view, name='home'),
    path('admin-dashboard/', admin_view, name='admin_view'),
    path('librarian-dashboard/', librarian_view, name='librarian_view'),
    path('member-dashboard/', member_view, name='member_view'),
]

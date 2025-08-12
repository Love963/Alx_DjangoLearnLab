from django.urls import path   # For URL routing
from django.contrib.auth import views as auth_views   # Import Django auth views (login/logout)
from .import views

urlpatterns = [
    # User registration URL 
    path('register/', views.register, name='register'),
    # User profile URL (views & update)
    path('profile/', views.profile, name='profile'),
    # Login page using  built-in LoginView; override template path
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    # Logout page using built-in LogoutView; override template path
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

]

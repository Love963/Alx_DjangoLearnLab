from django.shortcuts import render
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from .models import CustomUser
# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    
from django.shortcuts import render, redirect
from .models import User
from .models import Contact
from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import smtplib
import string
# Create your views here.
def index(request):
    return render(request, 'index.html')

def destination(request):
    return render(request, 'destination.html')

def video(request):
    return render(request, 'video.html')

def booking(request):
    return render(request, 'booking.html')

def login(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower().strip()  # Convert email to lowercase and trim whitespace
        password = request.POST.get('password').strip()  # Trim whitespace from password
        
        print("Email:", email)
        print("Password:", password)
        
        user = User.objects.filter(email__iexact=email).first()
        if user and user.verified is True:
            print("Stored Password:", user.password)
            if check_password(password, request.user.password):
                request.session['username'] = user.username  # Save user's ID in session
                return redirect('home')  # Redirect to dashboard or another page
            else:
                error_message = "Incorrect email or password. Please try again."
                print("Password did not match!")
                return render(request, "login.html", {'error_message': error_message})
        else:
            error_message = "User with this email does not exist."
            print("User not found:", email)
            return render(request, "login.html", {'error_message': error_message})
    return render(request, "login.html")

from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Host, Destination, Booking
from datetime import datetime
from .models import Contact
from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient
import random
import smtplib
import string


# Create your views here.
def index(request):
    return render(request, 'index.html')

def destination(request):
    destinations = Destination.objects.all()
    return render(request, 'destination.html', {'destinations': destinations})

def destination_detail(request, name):
    destination = get_object_or_404(Destination, name=name)
    return render(request, 'dest_info.html', {'destination': destination})

def video(request):
    return render(request, 'video.html')

def booking(request):
    destinations = Destination.objects.all()
    return render(request, 'booking.html',{'destinations': destinations})

def packagetype(request):
    return render(request, 'package.html')

# booking form
def book_trip(request):
    if request.method == 'POST':
        # Check if the user has a session key
        if 'email' in request.session:
            email = request.session['email']
            destination_name = request.POST.get('destination_name')
            package_type = request.POST.get('package_type')
            number_of_travelers = request.POST.get('number_of_travelers')
            date = request.POST.get('date')

            # Retrieve the destination based on the name
            destination = Destination.objects.get(name=destination_name)

            # Create a new Booking object
            booking = Booking(destination=destination, package_type=package_type, number_of_travelers=number_of_travelers, date=date, email=email)
            booking.save()
            booking_id = booking.booking_id
            print(booking_id)

            return render(request, 'booking_success.html')  # Redirect to a success page after booking
        else:
            return redirect('login')  # Redirect to the login page if the user does not have a session
    else:
        destinations = Destination.objects.all()  # Retrieve all destinations
        return render(request, 'booking.html', {'destinations': destinations})

def login(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()  # Convert email to lowercase and trim whitespace
        password = request.POST.get('password')  # Trim whitespace from password
        print("Email:", email)
        print("Password:", password)
        user = User.objects.filter(email__iexact=email).first()
        if user:
            print("Stored Password:", user.password)
            password_match = check_password(password, user.password)
            print(f"Password Match: {password_match}")
            if check_password(password, user.password):
                request.session['phone'] = user.phone
                request.session['email'] = user.email
                request.session['username'] = user.username
                return render(request, 'index.html')  # Redirect to dashboard or another page
            else:
                error_message = "Incorrect email or password. Please try again."
                print("Password did not match!")
                return render(request, "login.html", {'error_message': error_message})
        else:
            error_message = "User with this email does not exist or is not verified."
            print("User not found or not verified:", email)
            return render(request, "login.html", {'error_message': error_message})
    return render(request, "login.html")


def user_logout(request):
    logout(request)
    if 'phone' in request.session:
        del request.session['phone']
    return redirect('home')  # Redirect to the homepage or any other page after logout

# Register Page 

def register(request):
    return render(request, 'register.html')

def send_email(subject, message, recipient_email):
    sender_email = 'rohitchauhan9880@gmail.com'  # Update with your Gmail email
    sender_password = 'hrkdsjslmpyevisg'  # Update with your Gmail password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()

# View for user registration
def save_register(request):
    if request.method == "POST":
        username = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        otp_verified = request.POST.get('verified')  # Check if OTP is verified
        
        if otp_verified:
            try:
                user = User.objects.create_user(username=username, phone=phone, email=email, password=password)
                user.verified = True
                user.save()
                return render(request, 'registration_success.html', {'email': email})
            except IntegrityError:
                error_message = "This email address is already registered."
        else:
            otp = ''.join(random.choices(string.digits, k=6))
            try:
                user = User(username=username, phone=phone, email=email, password=make_password(password), otp=otp)
                user.save()
                subject = 'OTP Verification'
                message = f'Your OTP for registration is: {otp}'
                recipient_email = email
                send_email(subject, message, recipient_email)
                return render(request, 'otp.html', {'email': email})
            except IntegrityError:
                error_message = "This email address is already registered."
        return render(request, 'register.html', {'error_message': error_message})


# View for OTP verification
def otp(request, email):
    if request.method == "POST":
        # Get OTP entered by the user
        entered_otp = request.POST.get('otp')
        email = request.POST.get('email')
        # Retrieve the user objects by email
        user = User.objects.filter(email=email, otp=entered_otp).first()
        if user:
            user.verified = True
            user.save()
            return render(request, 'registration_success.html', {'email': user.email})
        else:
            return render(request, 'failure.html')
    else:
        return render(request, 'otp.html')

def contact(request):       
    return render(request, 'contact.html')

def sent_message(request):
    error_message = ""
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        mess = Contact(name = name, email = email, subject = subject, message = message)
        mess.save()
        try:
            subject = subject
            message = message
            recipient_email = "rohitchauhan9880@gmail.com"
            send_email(subject, message, recipient_email)
        except Exception as e:
            # Log the exception for debugging purposes
            print("Error:", e)
            error_message = "Message Sent Unsuccessful"  
    return render(request, 'contact.html', {'error_message' : error_message})

# Admin Code start here

# Login Page
def login1(request):
    return render(request, 'admintrav/login.html')

def loginview1(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()  # Convert email to lowercase and trim whitespace
        password = request.POST.get('password')  # Trim whitespace from password
        print("Email:", email)
        print("Password:", password)
        user = Host.objects.filter(email__iexact=email).first()
        if user:
            print("Stored Password:", user.password)
            password_match = check_password(password, user.password)
            print(f"Password Match: {password_match}")
            if check_password(password, user.password):
                request.session['email'] = user.email
                request.session['username'] = user.username
                return render(request, 'admintrav/index.html', {'current_datetime': current_datetime})  # Redirect to dashboard or another page
            else:
                error_message = "Incorrect email or password. Please try again."
                print("Password did not match!")
                return render(request, "admintrav/login.html", {'error_message': error_message})
        else:
            error_message = "User with this email does not exist or is not verified."
            print("User not found or not verified:", email)
            return render(request, "admintrav/login.html", {'error_message': error_message})
    return render(request, "admintrav/login.html")

# logout
def admin_logout(request):
    logout(request)
    if 'email' in request.session:
        del request.session['email']
    return redirect('dashboard')
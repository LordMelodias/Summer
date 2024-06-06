from django.shortcuts import render
from .models import Video, Comment, Channel, Like, Dislike, Video_View, Channel_Subscription, User
import string, random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
# Create your views here.

# Email setup
def send_email(subject, message, recipient_email):
    sender_email = 'rohitchauhan@gmail.com'  # Update with your Gmail email
    sender_password = '################'  # Update with your Gmail password

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


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'your_video/about.html')


def channel_video(request):
    return render(request, 'your_video/index.html')

def community(request):
    return render(request, 'your_video/community.html')

def video(request):
    return render(request, 'your_video/video.html')

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
                request.session['email'] = user.email
                request.session['name'] = user.name
                return render(request, 'your_video/index.html', )  # Redirect to dashboard or another page
            else:
                error_message = "Incorrect email or password. Please try again."
                print("Password did not match!")
                return render(request, "login.html", {'error_message': error_message})
        else:
            error_message = "User with this email does not exist or is not verified."
            print("User not found or not verified:", email)
            return render(request, "login.html", {'error_message': error_message})
    return render(request, "login.html")


def register(request):
    return render(request, 'register.html')

def save_register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        otp_verified = request.POST.get('verified')  # Check if OTP is verified
        
        if otp_verified:
            try:
                user = User.objects.create_user(name=name, email=email, password=password)
                user.verified = True
                user.save()
                return render(request, 'regsucessful.html', {'email': email})
            except IntegrityError:
                error_message = "This email address is already registered."
        else:
            otp = ''.join(random.choices(string.digits, k=6))
            try:
                user = User(name=name,  email=email, password=make_password(password), otp=otp)
                user.save()
                subject = 'OTP Verification'
                message = f'Your OTP for registration is: {otp}'
                recipient_email = email
                send_email(subject, message, recipient_email)
                return render(request, 'otp.html', {'email': email})
            except IntegrityError:
                error_message = "This email address is already registered."
        return render(request, 'register.html', {'error_message': error_message})


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
            return render(request, 'regsucessful.html', {'email': user.email})
        else:
            return render(request, 'failure.html')
    else:
        return render(request, 'otp.html')
    
 
from django.shortcuts import redirect, render
from .models import Video, Comment, Channel, Like, Dislike, Video_View, Channel_Subscription, User
import string, random
from django.views.generic.base import View, HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from venv import logger
from django.shortcuts import render, get_object_or_404
# Create your views here.

# Email setup
def send_email(subject, message, recipient_email):
    sender_email = 'rohitchauhan@gmail.com'  # Update with your Gmail email
    sender_password = '#############'  # Update with your Gmail password

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

def channel_video(request):
    email = request.session.get('email')
    if not email:
        logger.error("Email not found in session")
        return redirect('login')  # Redirect to login if no email in session

    try:
        user = get_object_or_404(User, email=email)
    except Exception as e:
        logger.error(f"User with email {email} not found: {e}")
        return redirect('register')  # Redirect to register if user not found

    try:
        channel = Channel.objects.get(user=user)
        request.session['name'] = channel.name
    except Channel.DoesNotExist:
        logger.info(f"Channel for user {email} not found, redirecting to channel creation page")
        return render(request, 'your_video/channel_create.html', {'email': email})  # Render channel creation page if channel not found
     
    video = Video.objects.filter(channel_name=channel.name).order_by('-upload_date')  # Order by upload date
    latest_video = video.first()
    context = {
        'channel': channel,
        'latest_video': latest_video,
        'video': video,
    }
    return render(request, 'your_video/index.html', context)


def channel_video(request):
    email = request.session.get('email', '')
    return render(request, 'your_video/index.html', {'email': email})

def community(request):
    return render(request, 'your_video/community.html')

def video(request):
    email = request.session.get('email')
    user = get_object_or_404(User, email=email)
    channel = Channel.objects.get(user=user)
    video = Video.objects.filter(channel_name=channel.name).order_by('-upload_date')  # Order by upload date
    context = {
        'channel': channel,
        'video': video,
    }
    return render(request, 'your_video/video.html',  context)

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
                return redirect('home')  # Redirect to dashboard or another page
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
    
def create_chan(request, email):
    email = request.session.get('email', '')
    return render(request, 'your_video/channel_create.html', {'email': email})

# create Channel
def create_channel(request, email):
    email = request.POST.get('email')
    # Ensure the session email matches the provided email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'User does not exist'})

    # Check if a channel already exists for the user
    channel = Channel.objects.filter(user=user).first()
    if channel:
        request.session['name'] = channel.name
        # If a channel already exists, redirect to the detail view
        return redirect('channel_video')

    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        try:
            channel = Channel(name=name, image=image, user=user)
            channel.save()
            request.session['name'] = channel.name
            return redirect('channel_video')  # Redirect to a view showing the created channel
        except IntegrityError as e:
            # Handle duplicate key error or other integrity errors
            return render(request, 'error.html', {'message': 'A channel with this email already exists or other integrity error'})           
            
# Uploaded video
def upload_video(request):
    if request.method == 'POST':
        # Get the email from the session
        email = request.session.get('email')
        
        # Retrieve the user object based on the email
        user = get_object_or_404(User, email=email)
        # Extract data from the request
        video_name = request.POST.get('name')
        video_description = request.POST.get('description')
        video_file = request.FILES.get('video')
        video_thumbnail = request.FILES.get('thumbnail')
        channel_name = request.POST.get('channel_name')
        
        # Get or create the channel object
        
        # Create the video object and associate it with the user and channel
        video = Video.objects.create(
            name=video_name,
            description=video_description,
            video_file=video_file,
            thumbnail=video_thumbnail,
            user=user,
            channel_name=channel_name
        )
        video.save()
        # Redirect to the channel_video view after successful upload
        return redirect('channel_video')
    
    # Render the upload form for GET requests
    return render(request, 'your_video/video_upload.html')

def play_video(request, name):
    email = request.session.get('email')
    user = get_object_or_404(User, email=email)
    channel = Channel.objects.get(user=user)
    video = Video.objects.get(name=name)
    video.name = video.name.replace(' ', '_')
    all_videos = Video.objects.all()
    context = {
        'channel': channel,
        'video': video,
        'all_videos': all_videos,
    }
    return render(request, 'video.html', context)
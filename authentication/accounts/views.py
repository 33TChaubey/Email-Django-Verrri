from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
# Create your views here.


def home(request):
    
    return render (request, 'home.html')


def login_attemp(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        user_obj = User.objects.filter(username=username).first()
        
        if user_obj is None:
            messages.success(request, "User Not Found")
            return redirect ('login')
        
        profile_obj = Profile.objects.filter(user=user_obj).first()
        
        if not profile_obj.is_verified:
            messages.success(request, "Profile is not verified check your mail")
            return redirect ('login')
        user = authenticate(username=username,password=password)
        if user is None:
            messages.success(request, "Wrong Password")
            return redirect ('login')
        login(request, user)
        return redirect('/')
    
    return render(request, 'login.html')


def register_attemp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            if User.objects.filter(username=username).first():
                messages.success(request, "Username is Taken")
                return redirect('register')
            
            if User.objects.filter(password=password).first():
                messages.success(request, "email is already taken")
                return redirect ('register')
            
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token= auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            
            return redirect ('token_send')
        except Exception as e:
            print(e)
        
    return render (request, 'register.html')
 
 
def success(request):
    return render (request, 'success.html')


def token_send(request):
    
    return render (request, 'token_send.html')


def error_page(request):
    
    return render (request, 'error.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, "This account is already exist")
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, "Congrats Bro! Your account has been successfully Verify")
            return redirect ('login')
        else:
            return redirect ('error')
    except Exception as e:
        print(e)
        return redirect ('/')
        
        


def send_mail_after_registration(email, auth_token):
    subject = "Your account need to be verify"
    message = f"hii paste the link the link to verify http://127.0.0.1:8000/verify/{auth_token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message,email_from,recipient_list)
    
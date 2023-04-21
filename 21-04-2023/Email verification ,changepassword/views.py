from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from .helpers import send_forgotpassword_email
from .forms import BookForm
from .models import Book,Profile
from django.contrib.auth.models import User,auth
import random
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
import http.client
# Create your views here.
def sendmail(emailid , token):
    send_mail(
    "Your accoount need to be verified",
    f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}',
    "madarapusathwika9@gmail.com",
     [emailid],
)
    return True

def sendforgetpasswordemail(emailid, token):
    send_mail(
    "Your forgetpassword link",
    f'Hi click on the link to reset your password http://127.0.0.1:8000/changepassword/{token}',
    "madarapusathwika9@gmail.com",
     [emailid],
    )
    return True


def forgetpassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forgetpassword')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            sendforgetpasswordemail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forgetpassword/')
                
    
    
    except Exception as e:
        print(e)
    return render(request , 'forgetpassword.html')

def register(request):
    if request.method =='POST':
        username=request.POST['username']
        emailid=request.POST['email']
        password=request.POST['password']
        mobile=request.POST['mobile']
        if User.objects.filter(username=username).first():
            messages.success(request, "Username already exists")
            return redirect('/register')
        if User.objects.filter(email=emailid).first():
            messages.success(request, "Email already exists")
            return redirect('/register')
        if Profile.objects.filter(mobile=mobile).first():
            messages.success(request, "Mobile Number  already exists")
            return redirect('/register')
        user_obj= User.objects.create(username=username,email=emailid)
        user_obj.set_password(password)
        user_obj.save()
        auth_token=str(uuid.uuid4())
        profile_obj=Profile.objects.create(user=user_obj,mobile=mobile,auth_token=auth_token)
        print(auth_token)
        profile_obj.save()
        sendmail(emailid,auth_token)
        return redirect("/token")
        
    
    return render(request,"register.html")


def verify(request,auth_token):
    profile_obj=Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,"Your account has already been verified")
            return redirect("/login")
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,"Your email has been verified")
        return redirect('/login')
    else:
        return redirect('/error')

def error_page(request):
    return render(request,"error.html")


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,email=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/books/upload")
        else:
            messages.info(request,'Invalid username or password')
            return redirect('/login')
    else:
      return render(request,"login.html")


def logout_user(request):
    auth.logout(request)
    return redirect('/login')

def send_otp(request):
    return render(request,"otp.html")


def success(request):
    return render(request,"success.html")

def token_send(request):
    return render(request,"token_send.html")



def changepassword(request , token):
    context = {}
    
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/changepassword/{token}')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/changepassword/{token}')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')
            
            
            
        
        
    except Exception as e:
        print(e)
    return render(request , 'changepassword.html' , context)


def upload_file(request):
    context={}
    if request.method=="POST":
        uploaded_files=request.FILES['document']
        fs=FileSystemStorage()
        name=fs.save(uploaded_files.name,uploaded_files)
        url=fs.url(name)
        print(url)
        context['url']=fs.url(name)

        print(uploaded_files.name)
    return render(request,'upload.html',context)

def book_list(request):
    books=Book.objects.all()
    return render(request,'book_list.html',{'books':books})

def upload_book(request):
    if request.method =="POST":
        form=BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/books")
    else:
        form=BookForm()
    return render(request,'upload_book.html',{'form':form})


def delete_book(request,pk):
    if request.method=='POST':
        book=Book.objects.get(pk=pk)
        book.delete()
        return redirect("/books")

def search(request):
    query=request.GET['query']
    book=Book.objects.filter(
          Q(title__icontains=query) |
          Q(author__icontains=query) 
        
     )
    return render(request,'search.html',{'book':book})

def recent(request):
     file = Book.objects.latest('id')
     return render(request,'recent.html',{'file':file})
    
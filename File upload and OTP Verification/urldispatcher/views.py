from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from .helpers import send_forgotpassword_email
from .forms import BookForm,PaymentForm
from .models import Book,Profile,Payment
from django.contrib.auth.models import User,auth
import random
import uuid
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth import authenticate, login,logout
import http.client as ht
import pyotp
from datetime import datetime,timedelta
import os
from twilio.rest import Client
import requests
import time
import razorpay
"""def sendsms(mobile, otp):
    account_sid = os.getenv('AC13e8c8bdfb96fa0c8aa7a5d3e0caecef')
    auth_token = os.getenv('4df7909fd701a3352a7ffac29ae1121f')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                              body='Your one time password is {otp}',
                              from_='+917981136626',
                              to=mobile
                          )

    return True"""

    

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

def sendotpemail(emailid, token):
    send_mail(
    " otp",
    f'Your otp is {token}',
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
        request.session['auth_token']=auth_token
        otp=str(random.randint(1000,9999))
        request.session['otp']=otp
        request.session['timeotp']=time.time()
        profile_obj=Profile.objects.create(user=user_obj,mobile=mobile,auth_token=auth_token)
        print(auth_token)
        profile_obj.save()
        print(otp)
        #send_otp(mobile, otp)
        sendotpemail(emailid,otp)
        request.session['mobile'] = mobile
        return redirect('/otp')
        
        #sendmail(emailid,auth_token)
        #return redirect("/token")
        
    
    return render(request,"register.html")

def send_otp(mobile , otp):
   # conn = ht.HTTPSConnection("api.msg91.com")
    headers = { 'content-type': "application/json" }
    url = "https://control.msg91.com/api/v5/otp=?template_id=64475585d6fc05551964a8c4&mobile="+mobile+"&authkey=395388A4jKfOcVx64468333P1&country=91"
    payload={
  
    }
    
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authkey": "395388A4jKfOcVx64468333P1"
    }
    

    response = requests.post(url,json=payload, headers=headers)
    print(response.text)
    """conn.request("GET", url , headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)"""
    

def otp(request):
    #mobile = request.session['mobile']
    #context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        #profile = Profile.objects.filter(mobile=mobile).first()
        profile=request.session.get('otp')
        if otp == profile:
            x=request.session.get('timeotp')
            if(time.time()-x>30):
                return redirect('/register')
            
            else:
                return redirect('/login')
        else:
            print('Wrong')
            messages.info(request,"Please enter correct otp")
            #context = {'message' : 'Wrong OTP' ,'mobile':mobile}
            return render(request,'otp.html' , context)
            
    context={'rem':30}
    return render(request,'otp.html' , context)



def verify(request,auth_token):
       profile=Profile.objects.filter(auth_token=auth_token).first()
       if profile:
        if profile.is_verified:
            messages.success(request,"Your account has already been verified")
            return redirect("/login")
        profile.is_verified=True
        profile.save()
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
        mobile=request.POST.get('mobile')
        user=auth.authenticate(username=username,email=email,password=password,mobile=mobile)
        if user is not None:
            #sendotp(request)
            request.session['username']=username
            return redirect('/books/upload')
           
        else:
            messages.info(request,'Invalid username or password')
            return redirect('/login')
    else:
      return render(request,"login.html")


def logout_user(request):
    auth.logout(request)
    return redirect('/login')


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

def payment(request):
    if request.method=='POST':
        context={}
        name=request.POST.get('name')
        amount = int(request.POST.get('amount'))*100
        #create razorpay client

        client=razorpay.Client(auth=('rzp_test_9s4Zto25Cg7mER','OpKR0SMt9jH4idZ7PqmUlkl7'))
        #creating order 
        respone_payment = client.order.create({'amount':amount, 'currency':'INR'})
        #response_payment =client.order.create(amount=order_amount,currency=order_curr)
        print(respone_payment)
        order_id= respone_payment['id']
        order_status= respone_payment['status']
        if order_status=='created':
            book_inst=Payment(name=name,amount=amount,order_id=order_id)
            book_inst.save()
            respone_payment['name']=name
            form=PaymentForm(request.POST)
            return render(request,'payment.html',{'form':form,'payment':respone_payment})
    form=PaymentForm()
    return render(request,'payment.html',{'form':form})

def paymentstatus(request):
    response=request.POST
    params_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
        }
    client=razorpay.Client(auth=('rzp_test_9s4Zto25Cg7mER','OpKR0SMt9jH4idZ7PqmUlkl7'))
    try:
        status=client.utility.verify_payment_signature(params_dict)
        book_obj=Book.objects.get(order_id=response['razorpay_order_id'])
        book_obj.razorpay_payment_id=response['razorpay_payment_id']
        book_obj.paid=True
        book_obj.save()
        return render(request,'payment_status.html',{'status':True})
    except:
        return render(request,"payment_status.html",{'status':False})
    
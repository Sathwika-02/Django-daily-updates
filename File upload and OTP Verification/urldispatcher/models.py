from django.db import models
from django.contrib.auth.models import User,AbstractUser
import os
from django.contrib.auth import get_user_model
from django.urls import reverse
from twilio.rest import Client
# Create your models here.
"""class StudentForm(models.Model):
    firstname=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    file=models.FileField()

    class Meta:
        db_table= "student"
    """
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=10)
    auth_token=models.CharField(max_length=100,)
    is_verified=models.BooleanField(default=False)
    forget_password_token=models.CharField(max_length=100,default='SOME STRING')
    created_at=models.DateTimeField(auto_now_add=True)
    #otp=models.CharField(max_length=6,default='SOME STRING')

   

    def __str__(self):
        return self.user.username
    

class Book(models.Model):
    title=models.CharField(max_length=50)
    author=models.CharField(max_length=100)
    pdf=models.FileField()
    cover=models.ImageField(blank=True,default="Add image url which is you want")
    


    def __str__(self):
        return self.title
    
    def delete(self,*args,**kwargs):
        self.pdf.delete()
        super().delete(*args,**kwargs)

class Payment(models.Model):
    name=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    order_id=models.CharField(max_length=100,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False)
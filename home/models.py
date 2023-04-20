from django.db import models

# Create your models here.
class Student(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField(max_length=20)
    mobile=models.CharField(max_length=10)

"""lass ToDo(models.Model):
    Title=models.CharField(max_length=100,blank=False)
    Description=models.TextField(blank=True)
    Date=models.DateField(blank=False)
    completed=models.BooleanField(default=False)"""
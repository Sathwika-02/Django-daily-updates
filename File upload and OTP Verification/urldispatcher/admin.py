from django.contrib import admin

# Register your models here.
from urldispatcher.models import Book,Profile,Payment
admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Payment)

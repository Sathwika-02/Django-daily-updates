"""
URL configuration for httpreq project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from urldispatcher.views import upload_file
from django.conf import settings
from django.conf.urls.static import static
from  urldispatcher import views
from django.urls import path,include
from django.contrib.auth.views import PasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.register,name='register'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('otp/',views.otp,name='otp'),
    path('token/',views.token_send,name='token_send'),
    path('success/',views.success,name='success'),
    path('logout',views.logout_user,name='logout_user'),
    path('upload/',views.upload_file,name='upload_file'),
    path('books/',views.book_list,name='book_list'),
    path('books/upload/',views.upload_book,name='upload_book'),
    path('books/<int:pk>',views.delete_book,name='delete_book'),
    path('search/',views.search,name='search'),
    path('recent/',views.recent,name='recent'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('error/',views.error_page,name='error_page'),
    path('forgetpassword/',views.forgetpassword,name='forgetpassword'),
    path('changepassword/<token>',views .changepassword,name='changepassword'),
    path('payment/',views.payment,name='payment'),
    path('status/',views.paymentstatus,name='payment_status'),
   

    
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include
from .views import register,send_user_message,login

urlpatterns = [
    path('register', register.as_view() ,name='register'),
    path('login', login.as_view() ,name='login'),
    path('send_message', send_user_message.as_view() ,name='send_user_message'),
]+static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)


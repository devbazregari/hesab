from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include
from .views import (
    register , send_user_message,login , DeleteDebts,show_user_message , home, DeleteMessage , SaveDebt , ShowDebt , ShowMyDebt,UpdateDebts,UpdateMessage)

urlpatterns = [
    path('register', register.as_view() ,name='register'),
    path('login', login.as_view() ,name='login'),
    path('send/message', send_user_message.as_view() ,name='send_user_message'),
    path('show/message', show_user_message.as_view() ,name='show_user_message'),
    path('save/debt', SaveDebt.as_view() ,name='save_debt'),
    path('show/debt/<str:mobile>', ShowDebt.as_view() ,name='show_debt'),
    path('show/my/debt', ShowMyDebt.as_view() ,name='show_my_debt'),
    path('update/debt/<str:mobile>', UpdateDebts.as_view() ,name='update_debt'),
    path('delete/debt/<int:money>/<int:debtor>', DeleteDebts.as_view() ,name='delete_debt'),
    path('update/message', UpdateMessage.as_view() ,name='update_message'),
    path('delete/message/<str:message>/<int:receiver>', DeleteMessage.as_view() ,name='delete_message'),
    path('test', home ,name='test'),
]+static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)


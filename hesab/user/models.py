from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Commen(models.Model):
    created_on = models.DateTimeField(default = datetime.now())
    class Meta:
        abstract = True 


class CustomUserManager(BaseUserManager):
    def create_user(self,password,**kwargs):
        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,password,**kwargs):
        user = self.create_user(password,**kwargs)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=60,blank=False,null=False)
    mobile = models.CharField(max_length=11 , blank=False , null=False , unique=True)
    media = models.ImageField(upload_to ='files/')
    notif = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.mobile

class MessageBox(Commen,models.Model):
    sender = models.ForeignKey(to=User,blank=False,null=False,on_delete=models.CASCADE , related_name='user_sender')
    receiver = models.ForeignKey(to=User,blank=False,null=False,on_delete=models.CASCADE , related_name='user_receiver')
    message = models.CharField(max_length=3000,blank=True,null=True)

    def __str__(self):
        return self.message

class Debt(Commen,models.Model):
    debtor = models.ForeignKey(to=User,blank=False,null=False,on_delete=models.CASCADE,related_name="debtor")
    creditor = models.ForeignKey(to=User,blank=False,null=False,on_delete=models.CASCADE,related_name="creditor")
    money = models.BigIntegerField(blank=False,null=False)
        

   
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin,Group
from django.utils.translation import override, ugettext_lazy as _
from cloudinary.models import CloudinaryField


# Create your models here.
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    pic=CloudinaryField(overwrite=True,null=True)
    email = models.EmailField(unique=True,max_length=255,blank=False)
    first_name = models.CharField(_('first name'),max_length=150,blank=True)
    last_name = models.CharField(_('last name'),max_length=150,blank=True)
    is_staff = models.BooleanField(_('staff status'),default=False)
    is_active = models.BooleanField(_('active'),default=False)
    is_superuser = models.BooleanField(_('superuser'),default=False)
    date_joined = models.DateTimeField(_('date joined'),default=timezone.now)
    usergroup = models.ForeignKey(Group,related_name="groups",on_delete=models.SET_NULL,null=True,blank=True)
    
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return self.first_name+" "+self.last_name



class Post(models.Model):
    title=models.TextField(max_length=200)
    writer=models.TextField(max_length=200,null=True,blank=True)
    content=models.TextField(max_length=20000)
    pic=CloudinaryField(overwrite=True,null=True,blank=True)
    show=models.BooleanField(default=True)
    
class Gallery(models.Model):
    gpic=CloudinaryField(overwrite=True,null=True,blank=True)   


class Products(models.Model):
    name=models.TextField(max_length=200)
    desc=models.TextField(max_length=20000)
    pic=CloudinaryField(overwrite=True,null=True,blank=True)
    price=models.IntegerField()
    isCctv=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.name    
class Members(models.Model):
    mpic=CloudinaryField(overwrite=True,null=True,blank=True)
    mname=models.TextField(max_length=30)
    mposition=models.TextField(max_length=30)
               
class Stats(models.Model):
    scustomer=models.IntegerField()
    ssells=models.IntegerField()
    sproducts=models.IntegerField()
    smembers=models.IntegerField()

class customer_review(models.Model):
    cusname=models.TextField(null=True)
    cuspic=CloudinaryField(overwrite=True,null=True,blank=True)
    cusreview=models.TextField(null=True)

class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product_wishlist=models.ManyToManyField(Products,related_name="Product_wishlist",blank=True)
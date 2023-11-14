from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, user_name, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('Email field must be set')
        if not user_name:
            raise ValueError('Username field must be set')
        
        email=self.normalize_email(email)
        email=email.lower()
        user=self.model(email=email, 
                        user_name=user_name.lower(),
                        first_name=first_name, 
                        last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, user_name, first_name, last_name, email, password=None):
        user = self.create_user(user_name,first_name, last_name, email, password=password)
        
        user.is_staff = True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin ):
    user_name=models.CharField(unique=True, max_length=200)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    bio=models.TextField(blank=True)
    followers=models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name="user_followers",
                                    blank=True,
                                    symmetrical=False)
    following=models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name="user_following",
                                    blank=True,
                                    symmetrical=False)

    profilePic=models.ImageField(upload_to="avatars/", null=True, blank=True)
    
    objects=UserManager()

    USERNAME_FIELD='user_name'
    REQUIRED_FIELDS=['first_name','last_name', 'email']
    
    def save(self, *args, **kwargs):
        if not self.profilePic:
            self.profilePic="avatars/avatar.png"
        super(User, self).save(*args,**kwargs)
        
    def num_of_followers(self):
        if self.followers.count():
            return self.followers.count()
        else:
            return 0
    
    def num_of_following(self):
        if self.following.count():
            return self.following.count()
        else:
            return 0
    
    def __str__(self):
        return self.user_name



from statistics import mode
from django.db import models
from email_login import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    number =models.CharField(max_length=20,null=True,blank=True)
    forget_password_token= models.CharField(max_length=100)


class Profile_Pic(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True)
    backgound_image = models.ImageField(upload_to='images/',null = True,blank = True)
    images= models.ImageField(upload_to='images/',null = True,blank =True)

    
    @property
    def imageURL(self):
        try:
            url = self.images.url
        except:
            url = ''
        return url
    @property
    def backgroundURL(self):
        try:
            url = self.backgound_image.url
        except:
            url =''
        return url

    def __str__(self):
        return self.user.email


class Blog(models.Model):
    tag_name = models.CharField(max_length=100,default='')
    blog_name = models.CharField(max_length=200,default='')
    created_date = models.DateTimeField(default=now)
    update_date =models.DateTimeField(auto_now_add=now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.blog_name[0:20]+'....'+'by '+self.user.email


class Post(models.Model):
    post_name =models.CharField(max_length=100,default='')
    tag_name = models.CharField(max_length=100,default='')
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    post_header= models.CharField(max_length=500,default='')
    post_content= models.CharField(max_length=500,default='')
    images= models.ImageField(upload_to='images/',blank =True)
    document =models.FileField(upload_to='File/',blank =True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='likes',blank=True)
    created_date = models.DateTimeField(default=now)
    update_date = models.DateTimeField(auto_now_add=now)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.post_name+'...'+'by'+ self.user.email

    
    @property
    def imageURL(self):
        try:
            url = self.images.url
        except:
            url = ''
        return url

    @property
    def documentURL(self):
        try:
            url = self.document.url
        except:
            url = ''
        return url


class Social(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True)
    linkedin = models.URLField(max_length=500)
    twitter= models.URLField(max_length=500)
    instagram = models.URLField(max_length=500)
    facebook = models.URLField(max_length=500)

    def __str__(self):
        return self.user.first_name

class About(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True)
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    workad_at = models.CharField(max_length=100)
    Studied_at = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.text[0:10]+'...'+'by '+ self.user.email



# SELECT * FROM accounts_customuser 
# INNER JOIN accounts_profile_pic ON accounts_customuser.id = accounts_profile_pic.user_id
# INNER JOIN accounts_social ON accounts_social.user_id = accounts_customuser.id
# INNER JOIN accounts_about ON accounts_about.user_id = accounts_customuser.id
# INNER JOIN accounts_post ON accounts_post.user_id = accounts_customuser.id

# {
# "email":"vikaskohli614@gmail.com",
# "username":"vikaskohli",
# "password":"misti@123",
# "first_name":"vikas",
# "last_name":"kohli",
# "number":"9876543212"
# }
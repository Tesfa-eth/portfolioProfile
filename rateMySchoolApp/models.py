from django.db import models

#from ast import mod
#from enum import auto
#from pyexpat import model
from django.utils import timezone
from sqlalchemy import null # get time zone
from django.contrib.auth.models import User # default user model
# Create your models here.

# Create your models here.
# After adding the models
# python manage.py makemigrations     : applys the model changes
# python manage.py migrate       : now it migrates all the models including the one I just created
# created super user
# username = Admin, password = Muler**********

# Extending User Model Using a One-To-One Link


class Universities(models.Model):
    name = models.CharField(max_length=100)
    #date_created = models.DateTimeField(auto_now_add=True)
    country_code = models.IntegerField() # will be using ISO 3166-1 country codes
    overall_rating = models.IntegerField()
    def __str__(self) -> str:
        return self.name


# profile
# firstName = models.CharField(default=null, max_length=20)
# lastName = models.CharField(default=null, max_length=20)
# verified = models.BooleanField(default=False)
# blocked = models.BooleanField(default=False)
# reported = models.IntegerField(default=0)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(default=null, max_length=20)
    lastName = models.CharField(default=null, max_length=20)
    # avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    verified = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    reported = models.IntegerField(default=0) 
    bagdeValue = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    postcontent = models.CharField(max_length=200)
    # Reminder: changed the the zone in settings.py from UTC to EST
    date_created = models.DateTimeField(auto_now_add=True)
    # postNum = models.IntegerField()
    upvoteCount = models.IntegerField(default=0)
    downvoteCount = models.IntegerField(default=0)
    rate_stars = models.IntegerField(default=0)

    # foriegn ID connected to the user and rated body
    ratedBody = models.ForeignKey(Universities, on_delete=models.CASCADE)
    raterUser = models.ForeignKey(User, on_delete=models.CASCADE)

   
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

class Universities(models.Model):
    name = models.CharField(max_length=100)
    #date_created = models.DateTimeField(auto_now_add=True)
    country_code = models.IntegerField() # will be using ISO 3166-1 country codes
    overall_rating = models.IntegerField()
    def __str__(self) -> str:
        return self.name



"""class Post(models.Model):
    postcontent = models.CharField(max_length=200)
    firstName = models.CharField(default=null, max_length=20)
    lastName = models.CharField(default=null, max_length=20)
    # Reminder: changed the the zone in settings.py from UTC to EST
    date_created = models.DateTimeField(auto_now_add=True)
    # user_id = models.IntegerField()
    # postNum = models.IntegerField()
    upvoteCount = models.IntegerField(default=0)
    downvoteCount = models.IntegerField(default=0)
    # ratedBodyID = models.IntegerField()
    rate_stars = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)

    # until username is created
    ratedBody = models.ForeignKey(Universities, on_delete=models.CASCADE)"""
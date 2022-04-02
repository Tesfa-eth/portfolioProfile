from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ratemySchool-index'),
    path('collegeRating/', views.college_rating, name='collegeRating'),
    path("home/", views.home, name="home"), # new
]
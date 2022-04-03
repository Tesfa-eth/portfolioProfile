from unicodedata import name
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='ratemySchool-index'),
    path('collegeRating/', views.college_rating, name='collegeRating'),
    path("home/", views.home, name="home"), # new
    path("accounts/", include("allauth.urls")), # new
]
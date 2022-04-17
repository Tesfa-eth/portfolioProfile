from unicodedata import name
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='ratemySchool-index'),
    path('collegeRating/', views.college_rating, name='collegeRating'),
    path("dashboard/", views.dashboard, name="dashboard"), 
    path("myratings/", views.myRatings, name="myratings"), 
    path('updatePost/<int:pk>/', views.updatePost, name="updatepost"), 
    path("profile/", views.profile, name="profile"), 
    path("accounts/", include("allauth.urls")),
]
from django.shortcuts import render, redirect
from .models import Universities


# Create your views here.
def index(request):
    """render the main page"""
    #return HttpResponse('<h1>Hello</h1>')
    return render(request,'rateMySchool/index.html')

from django.contrib.auth.models import User
def college_rating(request):
    """renders college rating page"""
    print(str(User.is_anonymous), "printing stuff")
    univeristies = Universities.objects.all()
    print
    context = {
        'universities' : univeristies,
    }
    return render(request, 'rateMySchool/collegeRating.html', context)

def home(request):
    return render(request, 'rateMySchool/home.html')

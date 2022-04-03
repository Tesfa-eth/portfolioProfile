from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
#@login_required #, if necessary
def dashboard(request):
    return render(request, 'rateMySchool/dashboard.html')

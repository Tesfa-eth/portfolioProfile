from django.shortcuts import render

from django.http import HttpResponse # temp

# Create your views here.
def index(request):
    """render the main page"""
    #return HttpResponse('<h1>Hello</h1>')
    return render(request,'rateMySchool/index.html')

def college_rating(request):
    """renders college rating page"""
    return render(request, 'rateMySchool/collegeRating.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Universities, Post


# Create your views here.
def index(request):
    """render the main page"""
    #return HttpResponse('<h1>Hello</h1>')
    return render(request,'rateMySchool/index.html')

from django.contrib.auth.models import User
def college_rating(request):
    """renders college rating page"""
    univeristies = Universities.objects.all()
    
    if 'collegeQuery' in request.GET:
        q = request.GET['collegeQuery']
        crude_data = Universities.objects.filter(name__icontains=q)
        print(crude_data, "sfffff")
        if len(crude_data) != 0: # if the search succeeds
            query_post = Post.objects.filter(ratedBody=crude_data[0])
            # debug
            # print(crude_data[0])
            # print(query_post, len(query_post), "query post")
            data = crude_data[0]
            #summary = get_summary(data)
            #print("data")
            
        
            

    context = {
        'universities' : univeristies,
    }
    return render(request, 'rateMySchool/collegeRating.html', context)

#@login_required #, if necessary
def dashboard(request):
    return render(request, 'rateMySchool/dashboard.html')

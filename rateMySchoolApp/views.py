from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Universities, Post
from django.contrib.auth.models import User # used in forms
from .forms import UniversityRateForm
import wikipediaapi

# Create your views here.
def index(request):
    """render the main page"""
    #return HttpResponse('<h1>Hello</h1>')
    return render(request,'rateMySchool/index.html')

def get_summary(name):
    """takes the title of university and returns a wiki summery"""
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(name)
    if page_py.exists():
        return page_py.summary
    else:
        return 'Wiki summary not found'

def matchRatings(data):
    """matches ratings data to lables"""
    matchedData = []
    lable = []
    lable.append("5-star")
    matchedData.append(data.count(5))
    lable.append("4-star")
    matchedData.append(data.count(4))
    lable.append("3-star")
    matchedData.append(data.count(3))
    lable.append("2-star")
    matchedData.append(data.count(2))
    lable.append("1-star")
    matchedData.append(data.count(1))
    
    return lable, matchedData

def Average(lst):
    """calculate average rating"""
    if len(lst) > 0:
        return sum(lst) / len(lst)
    else:
        return 0


def college_rating(request):
    """renders college rating page"""
    # Todo: make sure that one user can't rate a university more than once
    #     : numerical and text ratings should be overwritten
    summary = ''
    searchedUniversity = ''
    labledRatings = ''
    lable = ''
    average_rating = ''
    universityRatePosts = ''
    graph_data = []
    univeristies = Universities.objects.all()
    if 'collegeQuery' in request.GET:
        q = request.GET['collegeQuery']
        crude_data = Universities.objects.filter(name__icontains=q)
        if len(crude_data) != 0: # if the search succeeds
            # find posts related to university (formerly called query_post)
            universityPostRatings = Post.objects.filter(ratedBody=crude_data[0])
            # debug
            # print(crude_data[0])
            # print(query_post, len(query_post), "query post")
            # searched university (formerly called data)
            searchedUniversity = crude_data[0] # pick first
            summary = get_summary(searchedUniversity)
            
            # later should be ordered by users badge (Gold, Silver, Platinium)
            universityRatePosts = Post.objects.filter(ratedBody=searchedUniversity).order_by('-rate_stars')
            for post in universityRatePosts:
                graph_data.append(post.rate_stars)
            
            average_rating = Average(graph_data)
            # labled Ratings formerly graph_data
            lable, labledRatings = matchRatings(graph_data)

            print(average_rating, lable, labledRatings)
            
        
            

    context = {
        'universities' : univeristies,
        'wiki_summary': summary,
        'universities' : univeristies,
        'queryUNI' : searchedUniversity,
        'posts': universityRatePosts, # goes to displaying individual ratings of universities
        # chart data
        'graph_data': labledRatings,
        'lable': lable,
        'average_rating': average_rating,
    }
    return render(request, 'rateMySchool/collegeRating.html', context)

#@login_required #, if necessary
def dashboard(request):

    if request.method == 'POST':
        form = UniversityRateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.raterUser_id = request.user.id # connect it to the user
            obj.save()    #form.save()
            return redirect('/dashboard')
    else:
        form = UniversityRateForm()
    
    context = {
        'form': form,
    }
    return render(request, 'rateMySchool/dashboard.html', context)

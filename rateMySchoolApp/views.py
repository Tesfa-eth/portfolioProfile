import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Universities, Post
from django.contrib.auth.models import User # used in forms
from .forms import ReportPostForm, UniversityRateForm, EditUniversityRatePostForm, UserProfileManagementForm
import wikipediaapi
import logging

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
        average = sum(lst) / len(lst)
        return round(average,2)
    else:
        return 0


def college_rating(request):
    """renders college rating page"""
    # Todo: make sure that one user can't rate a university more than once
    #     : numerical and text ratings should be overwritten
    #     : make sure a user profile is created everytime a user signs up
    summary = ''
    searchedUniversity = ''
    labledRatings = ''
    lable = ''
    average_rating = ''
    universityRatePosts = ''
    graph_data = []
    univeristies = Universities.objects.all()
    test = 'test' # test printing
    test_dict = {'name': 'Tesfa', 'age': 44}
    
    test = ''
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
            raterUser = universityRatePosts[0].raterUser
            #raterProfile = Profile.objects.filter(user=raterUser)
            #test = raterProfile[0].verified
            for post in universityRatePosts:
                # user_id = post.raterUser.id
                # user_profile = Profile.objects.filter(user = user_id)
                # test = user_profile, user_id
                graph_data.append(post.rate_stars)
            
            average_rating = Average(graph_data)
            # labled Ratings formerly graph_data
            lable, labledRatings = matchRatings(graph_data)

            print(average_rating, lable, labledRatings)
            
        
            

    context = {
        'test_dict': test_dict,
        'test': test, # test printing
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
    if request.user.is_authenticated:
        userprofile = Profile.objects.filter(user = request.user.id)[0]
    else:
        userprofile = ''
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
        'userprofile': userprofile,
    }
    return render(request, 'rateMySchool/dashboard.html', context)

@login_required
def myRatings(request):
    """renders the user's ratings so far"""
    userPosts = Post.objects.filter(raterUser=request.user)
    context={
        'userPosts': userPosts
    }
    return render(request, 'rateMySchool/myratings.html', context)

@login_required
def profile(request):
    """renders the user's profile"""
    userprofile = Profile.objects.filter(user = request.user)[0]
    context={
        'userprofile': userprofile
    }
    return render(request, 'rateMySchool/profile.html', context)

@login_required
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    test = ''
    if request.method == 'POST':
        form = EditUniversityRatePostForm(request.POST, instance=post)
        if form.is_valid:
            obj = form.save(commit=False)
            obj.edited = True
            obj.save() 
            #form.save()
            return redirect('/collegeRating/')
    else:
        form = EditUniversityRatePostForm(instance=post)
    logging.debug("Edit button recieved")
    print("Edit button recieved")
    if request.user.is_superuser:
        test = True
    context = {
        'form': form,
        'test': test,
    }
    return render(request, 'rateMySchool/updatePost.html', context)

@login_required # restrict to admins only
def managePosts(request):
    posts = Post.objects.filter(reported=True).order_by('-reportedCount')
    context = {
        'posts': posts,
    }
    return render(request, 'rateMySchool/managePosts.html', context)

@login_required
def postDetail(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        'post':post
    }
    return render(request, 'rateMySchool/postDetail.html', context)

@login_required # restrict to admins only
def manageUserProfile(request, pk):
    # pk is the id of the user
    # get the profile id of the user
    userProfile = Profile.objects.filter(user = pk)[0]
    #userProfile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = UserProfileManagementForm(request.POST, instance=userProfile)
        if form.is_valid:
            form.save()
            return redirect('/managePosts/')
    else:
        form = UserProfileManagementForm(instance=userProfile)
    context = {
        'userProfile': userProfile,
        'form': form,
    }
    return render(request, 'rateMySchool/manageUserProfile.html', context)

@login_required
def reportConfirmation(request, pk):
    reportedPost = Post.objects.get(id=pk)
    alreadyReportedUsers = reportedPost.postreportedUsers.all()
    currentUserProfile = Profile.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        # update the reported to true!
        if currentUserProfile not in alreadyReportedUsers:
            reportedPost.postreportedUsers.add(currentUserProfile)
        else:
            reportedPost.postreportedUsers.remove(currentUserProfile)
        form = ReportPostForm(request.POST, instance=reportedPost)
        if form.is_valid:
            obj = form.save(commit=False)
            if len(reportedPost.postreportedUsers.all()) > 0:
                obj.reported = True
            else:
                obj.reported = False
            obj.save()
            return redirect('/collegeRating/')
    else:
        form = ReportPostForm(instance=reportedPost)
    context = {
        'alreadyreportedUsers':alreadyReportedUsers,
        'currentUserProfile': currentUserProfile,
    }
    return render(request, 'rateMySchool/reportConfirmation.html', context)

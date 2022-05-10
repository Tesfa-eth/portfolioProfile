import re
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import PostProfFeedback, Professor, Profile, Universities, Post
from django.contrib.auth.models import User # used in forms
from django.db.models import Count, Q
from .forms import EditUserProfile, ReportPostForm, UniversityRateForm, EditUniversityRatePostForm, UserProfileManagementForm, RemovePostForm
import wikipediaapi
import logging

# WARNING: this package has lots of warning and needs to be taken care of at some point
from profanity_check import predict, predict_prob

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
    #     : make sure a user profile is created everytime a user signs up (done)
    global searchQuery
    currentUserProfile = ''
    if request.user.is_authenticated:
        currentUserProfile = Profile.objects.filter(user=request.user)[0]
    summary = ''
    searchedUniversity = ''
    labledRatings = ''
    lable = ''
    average_rating = ''
    universityRatePosts = ''
    universityAcademicRatePosts = ''
    universitySocialRatePosts = ''
    universitySecurityRatePosts = ''
    averageAcademicRating = ''
    averageSocialRating = ''
    averageSecurityRating = ''
    graph_data = []
    univeristies = Universities.objects.all()
    test = 'test' # test printing
    test_dict = {'name': 'Tesfa', 'age': 44}
    
    test = ''
    search = False # if the user searched
    if 'collegeQuery' in request.GET:
        search = True
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
            universityAcademicRatePosts = Post.objects.filter(ratedBody=searchedUniversity,post_type='Academic').order_by('-rate_stars')
            universitySocialRatePosts = Post.objects.filter(ratedBody=searchedUniversity, post_type='Social').order_by('-rate_stars')
            universitySecurityRatePosts = Post.objects.filter(ratedBody=searchedUniversity, post_type='Security').order_by('-rate_stars')

            try:
                raterUser = universityRatePosts[0].raterUser
            except:
                raterUser = ''
            #raterProfile = Profile.objects.filter(user=raterUser)
            #test = raterProfile[0].verified
            academicratings = []
            for academicpost in universityAcademicRatePosts:
                academicratings.append(academicpost.rate_stars)
            averageAcademicRating = Average(academicratings)
            
            socialratings = []
            for socialpost in universitySocialRatePosts:
                socialratings.append(socialpost.rate_stars)
            averageSocialRating = Average(socialratings)

            securityratings = []
            for securitypost in universitySecurityRatePosts:
                securityratings.append(securitypost.rate_stars)
                
            averageSecurityRating = Average(securityratings)
            
            for post in universityRatePosts:
                # user_id = post.raterUser.id
                # user_profile = Profile.objects.filter(user = user_id)
                # test = user_profile, user_id
                graph_data.append(post.rate_stars)
            
            average_rating = Average(graph_data)
            # labled Ratings formerly graph_data
            lable, labledRatings = matchRatings(graph_data)

            print(averageSecurityRating, "Average security rat")

            print(average_rating, lable, labledRatings)
            
        
            

    context = {
        'search': search,
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
        'currentUserProfile': currentUserProfile,
        'universityAcademicRatePosts': universityAcademicRatePosts,
        'universitySocialRatePosts': universitySocialRatePosts,
        'universitySecurityRatePosts': universitySecurityRatePosts,
        'averageAcademicRating': averageAcademicRating,
        'averageSocialRating': averageSocialRating,
        'averageSecurityRating': averageSecurityRating,
    }
    return render(request, 'rateMySchool/collegeRating.html', context)

def professor_rating(request):
    test = ''
    professorRatePosts = professor = ''
    professors = Professor.objects.all()
    if request.user.is_authenticated:
        currentUserProfile = Profile.objects.filter(user=request.user)[0]
    if 'professorQuery' in request.GET:
        searchedprof = request.GET['professorQuery']
        #test = searchedprof
        professor = Professor.objects.filter(name__icontains=searchedprof)[0]
        professorRatePosts = PostProfFeedback.objects.filter(ratedProf=professor).order_by('-rate_stars')

    context = {
        'test': test,
        'professors': professors, # for search recommendation
        'professor': professor,
        'professorRatePosts': professorRatePosts,
        'currentUserProfile':currentUserProfile,
    }
    return render(request, 'rateMySchool/professorRating.html', context)

def profanityLabler(prob, prelable):
    """lables what should be done with the profanity probability result"""
    result = ''
    if prob < 0.5 and prelable == 0:
        result = 'clean'
    elif 0.5 <= prob < 0.75:
        result = 'report'
    elif prob >= 0.75 or prelable == 1:
        result = 'reportAndremove'
    return result

def profanityProb(text):
    """returns the probability of profanity of a cetain text"""
    return predict_prob([text])[0], predict([text])[0]

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
            #print(profanityProb(obj.postcontent), "post content")
            prob, prelable = profanityProb(obj.postcontent)
            profanityResult = profanityLabler(prob, prelable)
            obj.profanity_prob = round(prob*100, 4)
            if profanityResult == 'report':
                obj.auto_reported = True
            elif profanityResult == 'reportAndremove':
                obj.auto_reported = True
                obj.removed = True
            obj.save() 
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
    userPosts = Post.objects.filter(raterUser=request.user).order_by('-date_last_edited')
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
def editProfile(request):
    """edit user profile"""
    userprofile = Profile.objects.filter(user = request.user)[0]
    if request.method == 'POST':
        form = EditUserProfile(request.POST, instance=userprofile)
        if form.is_valid():   
            form.save()
            return redirect('/profile')
    else:
        form = EditUserProfile(instance=userprofile)
    context = {
        'test':'test',
        'form': form,
    }
    return render(request, 'rateMySchool/editProfile.html', context)


@login_required
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    test = ''
    if request.method == 'POST':
        form = EditUniversityRatePostForm(request.POST, instance=post)
        if form.is_valid:
            obj = form.save(commit=False)
            obj.edited = True
            #print(profanityProb(obj.postcontent), "post content")
            prob, prelable = profanityProb(obj.postcontent)
            profanityResult = profanityLabler(prob, prelable)
            obj.profanity_prob = round(prob*100, 4)
            if profanityResult == 'report':
                obj.auto_reported = True
            elif profanityResult == 'reportAndremove':
                obj.auto_reported = True
                obj.removed = True
                obj.save()
                return redirect('/updatePost/' + str(pk) + '/')
            obj.save() 
            return redirect('/myratings/')
    else:
        form = EditUniversityRatePostForm(instance=post)
    logging.debug("Edit button recieved")
    print("Edit button recieved")
    # if request.user.is_superuser:
    #     test = True
    context = {
        'form': form,
        'post': post,
        'test': test,
    }
    return render(request, 'rateMySchool/updatePost.html', context)

@login_required # restrict to admins only
def managePosts(request):
    """WARNING: updates in the detail section change the the last modified date"""
    # TODO: need to create a separate table called PostStatus. 
    # find reported, and sort by how many times each are reported.
    logic = Q(reported=True, auto_reported=True, _connector=Q.OR)
    posts = Post.objects.filter(logic).annotate(report_count=Count('postreportedUsers')).order_by('-report_count')
    
    context = {
        'posts': posts,
    }
    return render(request, 'rateMySchool/managePosts.html', context)

@login_required
def postDetail(request, pk):
    post = Post.objects.get(id=pk)
    alreadyReportedUsers = post.postreportedUsers.all()
    if request.method == 'POST':
        form = RemovePostForm(request.POST, instance=post)
        if form.is_valid:
            form.save()
            return redirect('/postdetail/' + str(pk) + '/')
    else:
        form = RemovePostForm(instance=post)
    context = {
        'post':post,
        'alreadyReportedUsers': alreadyReportedUsers,
        'form': form,
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
        'reportedPost': reportedPost,
        'alreadyreportedUsers':alreadyReportedUsers,
        'currentUserProfile': currentUserProfile,
    }
    return render(request, 'rateMySchool/reportConfirmation.html', context)


# @login_required
# def upvote(request, pk):
#     upvotedPost = Post.objects.get(id=pk)
#     alreadyUpvotedUsers = upvotedPost.upvote.all()
#     alreadyDownvotedUsers = upvotedPost.downvote.all()
#     currentUserProfile = Profile.objects.filter(user=request.user)[0]

#     # if request.method == 'POST':
#     # update the reported to true!
#     if currentUserProfile not in alreadyUpvotedUsers:
#         upvotedPost.upvote.add(currentUserProfile)
#     if currentUserProfile in alreadyUpvotedUsers:
#         upvotedPost.upvote.remove(currentUserProfile)
#     if currentUserProfile in alreadyDownvotedUsers:
#         upvotedPost.downvote.remove(currentUserProfile)
#     next = request.POST.get('next', '/')
#     print(next)
#     return redirect(request.META.get('HTTP_REFERER'))
#     #return redirect(request.META.get('HTTP_REFERER'))

# @login_required
# def downvote(request, pk):
#     downvotedPost = Post.objects.get(id=pk)
#     alreadyUpvotedUsers = downvotedPost.upvote.all()
#     alreadyDownvotedUsers = downvotedPost.downvote.all()
#     currentUserProfile = Profile.objects.filter(user=request.user)[0]

#     # if request.method == 'POST':
#     # update the reported to true!
#     if currentUserProfile not in alreadyDownvotedUsers:
#         downvotedPost.downvote.add(currentUserProfile)
#     if currentUserProfile in alreadyDownvotedUsers:
#         downvotedPost.downvote.remove(currentUserProfile)
#     if currentUserProfile in alreadyUpvotedUsers:
#         downvotedPost.upvote.remove(currentUserProfile)
#     return redirect(request.META.get('HTTP_REFERER'))


@login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        downvotechanges = False # checks if downvote gets updated
        likecolor = '#0275d8' # bootstrap primary
        id = int(request.POST.get('postid')) # post id
        post = Post.objects.get(id=id)
        alreadyUpvotedUsers = post.upvote.all()
        alreadyDownvotedUsers = post.downvote.all()
        currentUserProfile = Profile.objects.filter(user=request.user)[0]
        
        if currentUserProfile not in alreadyUpvotedUsers:
            post.upvote.add(currentUserProfile)
            likecolor = 'white'
        if currentUserProfile in alreadyUpvotedUsers:
            post.upvote.remove(currentUserProfile)
            likecolor = '#0275d8'
        if currentUserProfile in alreadyDownvotedUsers:
            post.downvote.remove(currentUserProfile)
            likecolor = '#0275d8'
            downvotechanges = True
        
        # post.save()
        dislikecount = post.downvote.all().count()
        likecount = post.upvote.all().count()
        #print("dislike result here: ", result, "post content: ", post.postcontent)

        return JsonResponse({'likecount': likecount,'dislikecount':dislikecount,
        'downvotechanges':downvotechanges, 'likecolor': likecolor,})


@login_required
def dislike(request):
    if request.POST.get('action') == 'post':
        #result = ''
        upvotechanges = False # upvote changes
        likecolor = '#0275d8' # bootstrap primary
        id = int(request.POST.get('postid')) # post id
        post = Post.objects.get(id=id)
        alreadyUpvotedUsers = post.upvote.all()
        alreadyDownvotedUsers = post.downvote.all()
        currentUserProfile = Profile.objects.filter(user=request.user)[0]

        if currentUserProfile not in alreadyDownvotedUsers:
            post.downvote.add(currentUserProfile)
        if currentUserProfile in alreadyDownvotedUsers:
            post.downvote.remove(currentUserProfile)
        if currentUserProfile in alreadyUpvotedUsers:
            post.upvote.remove(currentUserProfile)
            upvotechanges = True

        dislikecount = post.downvote.all().count()
        likecount = post.upvote.all().count()
        #print("dislike result here: ", result, "post content: ", post.postcontent)

        return JsonResponse({'likecount': likecount,'dislikecount':dislikecount,
        'upvotechanges':upvotechanges, 'likecolor': likecolor,})


@login_required
def proflike(request):
    if request.POST.get('action') == 'post':
        downvotechanges = False # checks if downvote gets updated
        likecolor = '#0275d8' # bootstrap primary
        id = int(request.POST.get('postid')) # post id
        post = PostProfFeedback.objects.get(id=id)
        alreadyUpvotedUsers = post.upvote.all()
        alreadyDownvotedUsers = post.downvote.all()
        currentUserProfile = Profile.objects.filter(user=request.user)[0]
        
        if currentUserProfile not in alreadyUpvotedUsers:
            post.upvote.add(currentUserProfile)
            likecolor = 'white'
        if currentUserProfile in alreadyUpvotedUsers:
            post.upvote.remove(currentUserProfile)
            likecolor = '#0275d8'
        if currentUserProfile in alreadyDownvotedUsers:
            post.downvote.remove(currentUserProfile)
            likecolor = '#0275d8'
            downvotechanges = True
        
        # post.save()
        dislikecount = post.downvote.all().count()
        likecount = post.upvote.all().count()
        #print("dislike result here: ", result, "post content: ", post.postcontent)

        return JsonResponse({'likecount': likecount,'dislikecount':dislikecount,
        'downvotechanges':downvotechanges, 'likecolor': likecolor,})


@login_required
def profdislike(request):
    if request.POST.get('action') == 'post':
        #result = ''
        upvotechanges = False # upvote changes
        likecolor = '#0275d8' # bootstrap primary
        id = int(request.POST.get('postid')) # post id
        post = PostProfFeedback.objects.get(id=id)
        alreadyUpvotedUsers = post.upvote.all()
        alreadyDownvotedUsers = post.downvote.all()
        currentUserProfile = Profile.objects.filter(user=request.user)[0]

        if currentUserProfile not in alreadyDownvotedUsers:
            post.downvote.add(currentUserProfile)
        if currentUserProfile in alreadyDownvotedUsers:
            post.downvote.remove(currentUserProfile)
        if currentUserProfile in alreadyUpvotedUsers:
            post.upvote.remove(currentUserProfile)
            upvotechanges = True

        dislikecount = post.downvote.all().count()
        likecount = post.upvote.all().count()
        #print("dislike result here: ", result, "post content: ", post.postcontent)

        return JsonResponse({'likecount': likecount,'dislikecount':dislikecount,
        'upvotechanges':upvotechanges, 'likecolor': likecolor,})

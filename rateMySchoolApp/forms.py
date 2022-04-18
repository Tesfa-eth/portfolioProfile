from cProfile import label
from pyexpat import model
from django import forms
from .models import Post, Profile, Universities
from django.contrib.auth.models import User


class UniversityRateForm(forms.ModelForm):
    univeristies = Universities.objects.all() # get universities
    #postcontent = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'What do you think about the college?'}))
    postcontent = forms.Textarea()
    # foriegn key as a dropdown
    ratedBody = forms.ModelChoiceField(label='Which university would you like to rate?', queryset=univeristies)
    #raterUser = User
    rate_stars = forms.IntegerField()
    
    class Meta:
        model = Post
        fields = ['ratedBody', 'postcontent', 'rate_stars']


class EditUniversityRatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postcontent', 'rate_stars']

class UserProfileManagementForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['blocked']
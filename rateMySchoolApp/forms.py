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
    rate_stars = forms.IntegerField(max_value=5, min_value=1)

    #fields = ['ratedBody', 'post_type', 'postcontent', 'rate_stars']
        # post types
        
    def __init__(self, *args, **kwargs):
        super(UniversityRateForm, self).__init__(*args, **kwargs)
        #post_types = ('General', 'Academic', 'Social', 'Security')
        post_types = [('General', 'General'), ('Academic', 'Academic'), ('Social', 'Social'), ('Security', 'Security')]
        #portfolios = [('pf 1', 'pf 1'), ('pf 2', 'pf 2'), ('pf 3', 'pf 3')]

        self.fields['post_type'] = forms.ChoiceField(
                    widget=forms.RadioSelect(),
                    choices=post_types,
                    required=False,
                    )
    
    class Meta:
        model = Post
        fields = ['ratedBody', 'post_type', 'postcontent', 'rate_stars']

class EditUniversityRatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postcontent', 'rate_stars']

class EditUserProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstName', 'lastName', 'bio']

class UserProfileManagementForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['blocked']

class ReportPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['reported']

class RemovePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['removed']
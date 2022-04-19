from django.contrib import admin
from .models import Universities, Profile, Post
# Register your models here.

# customize post model
class PostAdmin(admin.ModelAdmin):
    list_display = ('postcontent', 'raterUser', 'rate_stars', 'date_last_edited', 'upvoteCount', 'downvoteCount', 'reported', 'reportedCount')
    list_filter = ['reported', 'reportedCount']

# add the model I just imported to the adminstrative panel
admin.site.register(Post, PostAdmin)
admin.site.register(Universities)
admin.site.register(Profile)

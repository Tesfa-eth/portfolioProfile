# # creates profiles to existing users
# from django.contrib.auth.models import User
# from rateMySchoolApp.models import Profile

# users = User.objects.filter(profile=None)
# print("creating profiles for" + len(users) + "users")
# for user in users:
#     Profile.objects.create(user=user)

# print("completed successfully!")
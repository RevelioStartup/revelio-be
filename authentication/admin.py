from django.contrib import admin
from .models import AppUser, Profile, UserToken

# Register your models here.

admin.site.register(AppUser)
admin.site.register(Profile)
admin.site.register(UserToken)
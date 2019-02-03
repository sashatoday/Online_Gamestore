from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from gamestore.models import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(GameState)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(Purchase)
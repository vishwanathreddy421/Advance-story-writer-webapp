from django.contrib import admin
from .models import Story,UserProfile
class StoryAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass
# Register your models here.
admin.site.register(Story, StoryAdmin)
admin.site.register(UserProfile, UserProfileAdmin)



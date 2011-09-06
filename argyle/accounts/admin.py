from django.contrib import admin
from accounts.models import UserProfile

admin.autodiscover()

class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user','bio', 'birthday', 'city', 'country']
    
admin.site.register(UserProfile, UserProfileAdmin)

from django.contrib import admin
from accounts.models import UserProfile

admin.autodiscover()

class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user','bio', 'birthday', 'city', 'country', 'activation_code', 'key_expires']
    
admin.site.register(UserProfile, UserProfileAdmin)

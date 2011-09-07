from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name="User")
    bio = models.TextField("About Me", blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    
    city = models.CharField("City", max_length=30, blank=True, null=True)    
    country = models.CharField("Country", max_length=30, blank=True, null=True)

    activation_code = models.CharField(max_length=100, blank=True, null=True)
    key_expires = models.DateTimeField(blank=True,null=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __unicode__(self):
        return self.user.username
    
    @property
    def fullname(self):
        return self.user.get_full_name()
    
    @property
    def email(self):
        return self.user.email
    
    @property
    def age(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days / 365.25  )

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

from django import forms
from accounts.models import UserProfile
from django.forms.extras.widgets import SelectDateWidget
from datetime import date

year  = date.today().year
YEARS = range(year-18, year-100, -1) # only let people aged 18-100 register. :D

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)
    
class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = UserProfile
        fields = ['birthday', 'city', 'country', 'bio']
    

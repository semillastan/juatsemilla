from django import forms
from datetime import date
from core.models import *

year  = date.today().year
YEARS = range(year-18, year-100, -1) # only let people aged 18-100 register. :D

class LoginForm(forms.Form):
    file = forms.FileField()

    

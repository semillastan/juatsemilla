from django.conf.urls.defaults import *

from accounts.views import *
from helpers.utils import replace_urlpattern

urlpatterns = patterns('',
    #url(r'^', include('registration.urls')), #backends.default.
    url(r'^profile/$', profile, name='profile'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', register, name='register'),
    
)

#replacement = url(r'^register/$', register,
#                 {'backend': 'registration.backends.default.DefaultBackend', 'form_class': RegistrationForm },
#                 name='registration_register')
                 
#replace_urlpattern(urlpatterns, replacement)

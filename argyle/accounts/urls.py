from django.conf.urls.defaults import *

from accounts.views import *
from helpers.utils import replace_urlpattern

urlpatterns = patterns('',
    #url(r'^', include('registration.urls')), #backends.default.
    url(r'^profile/$', profile, name='profile'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^activate/$', activate, name='activate'),
    url(r'^activate/(?P<code>[\w|-]+)/$', activate, name='activate'),
    url(r'^activate/resend/(?P<username>[\w|-]+)/$', resend_activate, name='resend-code'),
    
)


from django.conf.urls.defaults import *

from core.views import *

urlpatterns = patterns('',
    url(r'^xml/$', xml, name='xml'),
    
)

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

urlpatterns = patterns('website.views',
    url(r'^$', direct_to_template, {'template':'home.html'}, name='home'),
    url(r'^done', 'done', name='done'),
)

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

urlpatterns = patterns('website.views',
    url(r'^$', 'root', name='root'),
    url(r'^home/?', 'oauthed_home', name='oauthed_home'),
    url(r'^rss/(?P<user_hash>.*)/?', 'get_favorites_rss', name='rss_favorites'),
    url(r'^is-authed/(?P<twitter_name>.*)/?$', view='is_authed', name='is-authed'),
    #url(r'^done', 'done', name='done'),
    url(r'^oauth/$',
        view='auth',
        name='twitter_oauth_auth'),

    url(r'^return/$',
        view='return_',
        name='twitter_oauth_return'),
)

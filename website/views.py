from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.feedgenerator import Rss201rev2Feed as RssFeed
import oauth, httplib, time, datetime
from twitter_app.utils import *
from website.models import OauthUser


try:
    import simplejson
except ImportError:
    try:
        import json as simplejson
    except ImportError:
        try:
            from django.utils import simplejson
        except:
            raise "Requires either simplejson, Python 2.6 or django.utils!"

CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
CONNECTION = httplib.HTTPSConnection(SERVER)

def root(request):
    return direct_to_template(request, 'root.html')

def oauthed_home(request):
    twitter_name = request.session.get('twitter_name', None)
    if twitter_name == None:
        # add message about needing to authenticate
        return HttpResponseRedirect('/')
    ou = OauthUser.objects.get(twitter_name=request.session['twitter_name'])
    fav_json = favorite_list(request, twitter_name)
    return render_to_response('oauthed_home.html', {'rss_link':reverse('rss_favorites', args=[ou.user_hash])}, context_instance=RequestContext(request))
    #    return HttpResponseRedirect('/')
    #return HttpResponseRedirect('/home/%s' % request.session['twitter_name'])
#    c = {'feed_url': None} # reverse of the feed view, passing in the twitter username
#    return render_to_response('oauthed_home.html', c, context_instance=RequestContext(request))

def get_favorites_rss(request, user_hash):
    ou = OauthUser.objects.get(user_hash=user_hash)
    favs = favorite_list(request, ou.twitter_name)
    feed = RssFeed(title='%s\'s favorites' % (ou.twitter_name), link='http://savethisfor.me/', description='')
    for f in favs:
        feed.add_item(title='%s - %s' % (f['user']['name'], f['created_at']), 
                      link='http://twitter.com/%s/status/%s' % (f['user']['screen_name'], f['id']),
                      description = f['text'],
                      author_name = f['user']['name'],
                      author_link = 'http://twitter.com/%s' % (f['user']['screen_name'],),
                      pubdate = datetime.datetime.strptime(f['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
    response = HttpResponse(mimetype='text/rss+xml')
    feed.write(response, 'UTF-8')
    return response

def auth(request):
    "/oauth/"
    OauthUser.objects.get_or_create(twitter_name=request.POST['twitter_name'])[0].save()
    request.session['twitter_name'] = request.POST['twitter_name']
    token = get_unauthorised_request_token(CONSUMER, CONNECTION)
    auth_url = get_authorisation_url(CONSUMER, token)
    response = HttpResponseRedirect(auth_url)
    request.session['unauthed_token'] = token.to_string()   
    return response

def return_(request):
    "/return/"
    unauthed_token = request.session.get('unauthed_token', None)
    if not unauthed_token:
        return HttpResponse("No un-authed token cookie")
    token = oauth.OAuthToken.from_string(unauthed_token)   
    if token.key != request.GET.get('oauth_token', 'no-token'):
        return HttpResponse("Something went wrong! Tokens do not match")
    access_token = exchange_request_token_for_access_token(CONSUMER, CONNECTION, token)
    response = HttpResponseRedirect(reverse('oauthed_home'))
    request.session['access_token'] = access_token.to_string()
    ou = OauthUser.objects.get(twitter_name=request.session['twitter_name'])
    ou.oauth_key = request.session['access_token']
    ou.save()
    return response

def tweet_feed(request):
    pass
    # from tweet model get all the users tweets
    # send them to a feed generator app that adds in the buttons

# ajax method
def remove_from_favorites(request):
    pass
    # remove the tweet from the user's favorites on twitter






def favorite_list(request, twitter_name=None):
    if twitter_name == None:
        access_token = request.session.get('access_token', None)
    else:
        ou = get_object_or_404(OauthUser, twitter_name__exact=twitter_name)
        access_token = ou.oauth_key
    if not access_token:
        return HttpResponse("You need an access token!")
    token = oauth.OAuthToken.from_string(access_token)   
    
    # Check if the token works on Twitter
    auth = is_authenticated(CONSUMER, CONNECTION, token)
    if auth:
        # Load the credidentials from Twitter into JSON
        creds = simplejson.loads(auth)
        page = 0
        friends = get_favorites(CONSUMER, CONNECTION, token, page, creds['screen_name'])
            
        # Load into JSON
        json = simplejson.loads(friends)

    return json
    #return render_to_response('oauthed_home.html', {'debug': json, 'rss_link':'/home/tsaylor/rss'})


def is_authed(request, twitter_name = None):
    ou = get_object_or_404(OauthUser, twitter_name__exact=twitter_name)
    access_token = ou.oauth_key
    if not access_token:
        return HttpResponse("You need an access token!")
    token = oauth.OAuthToken.from_string(access_token)   
    
    # Check if the token works on Twitter
    auth = is_authenticated(CONSUMER, CONNECTION, token)
    if auth:
        return HttpResponse("You are authenticated.")
    else:
        return HttpResponse("You are not authenticated.")

from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
import oauth, httplib, time, datetime
from twitter_app.utils import *

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

def home(request):
	return direct_to_template(request, 'home.html')

def oauthed_home(request):
    c = {'feed_url': None} # reverse of the feed view, passing in the twitter username
    return render_to_response('oauthed_home.html', c, context_instance=RequestContext(request))

def auth(request):
    "/oauth/"
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
    return response

def tweet_feed(request):
    pass
    # from tweet model get all the users tweets
    # send them to a feed generator app that adds in the buttons

# ajax method
def remove_from_favorites(request):
    pass
    # remove the tweet from the user's favorites on twitter

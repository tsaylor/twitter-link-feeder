from django.contrib import admin
from website.models import OauthUser, Tweet

admin.site.register(OauthUser)
admin.site.register(Tweet)

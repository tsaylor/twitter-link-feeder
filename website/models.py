from django.db import models

class OauthUser(models.Model):
    twitter_name = models.CharField(max_length=20)
    oauth_key = models.CharField(max_length=255)
    

class Tweet(models.Model):
    user = models.ForeignKey(OauthUser)
    message = models.CharField(max_length=140)
    data_dump = models.TextField()

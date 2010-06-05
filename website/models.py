from django.db import models
import hashlib

class OauthUser(models.Model):
    twitter_name = models.CharField(max_length=20)
    oauth_key = models.CharField(max_length=255, blank=True)
    user_hash = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.oauth_key:
            self.user_hash = hashlib.sha256(self.twitter_name+self.oauth_key).hexdigest()
        super(OauthUser, self).save(*args, **kwargs)
    

class Tweet(models.Model):
    user = models.ForeignKey(OauthUser)
    message = models.CharField(max_length=140)
    data_dump = models.TextField()

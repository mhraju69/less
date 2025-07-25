# airdrop/models.py

from django.db import models

class Participant(models.Model):
    wallet = models.CharField(max_length=255, unique=True)
    twitter = models.CharField(max_length=255)
    retweet = models.CharField(max_length=255)
    telegram = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=10, unique=True)
    referred_by = models.CharField(max_length=10, blank=True, null=True)
    points = models.PositiveIntegerField(default=0)
    pin = models.PositiveIntegerField()
    joined_at = models.DateTimeField(auto_now_add=True)

    def refarral_count(self):
        return Participant.objects.filter(referred_by=self.referral_code).count()
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from model_utils.models import TimeStampedModel


class Profile(TimeStampedModel):
    user = models.OneToOneField(User)
    twitter = models.CharField(max_length=15, null=True, blank=True)
    api_token = models.CharField(max_length=255)

    class Meta:
        db_table = 'profile'


#@receiver(post_save, sender=get_user_model())
#def create_auth_token(sender, instance=None, created=False, **kwargs):
#    if created:
#        Token.objects.create(user=instance)
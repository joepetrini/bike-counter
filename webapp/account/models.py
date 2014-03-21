from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel


class Profile(TimeStampedModel):
    user = models.OneToOneField(User)
    twitter = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = 'profile'
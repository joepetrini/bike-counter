import uuid
import hmac
from hashlib import sha1
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel


class Token(TimeStampedModel):
    """
    The default authorization token model.
    """
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'token'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        unique = str(uuid.uuid4())
        return hmac.new(unique, digestmod=sha1).hexdigest()

    def __unicode__(self):
        return _(self.key)


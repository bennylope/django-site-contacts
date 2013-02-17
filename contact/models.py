from django.db import models
from django.conf import settings
from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

def get_user_model():
    """Fill-in for functionality not available in Django < 1.5"""
    try:
        klass = get_model(USER_MODEL.split('.')[0], USER_MODEL.split('.')[1])
    except:
        raise ImproperlyConfigured("Your user class, {0}, is improperly defined".format(USER_MODEL))
    return klass


class Recipient(models.Model):
    """
    A model for determining which users will recieve contact messages from the
    contact form.
    """
    user = models.ForeignKey(USER_MODEL)

    def __unicode__(self):
        return u"{0}".format(self.user)

    class Meta:
        verbose_name = 'contact recipient'
        verbose_name_plural = 'contact recipients'

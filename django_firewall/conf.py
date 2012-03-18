'''
thanks: https://github.com/gregmuellegger/django-mobile/blob/master/django_mobile/conf.py for file layout
'''
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings
import datetime

class SettingsProxy(object):
    def __init__(self, settings, defaults):
        self.settings = settings
        self.defaults = defaults

    def __getattr__(self, attr):
        try:
            return getattr(self.settings, attr)
        except AttributeError:
            try:
                return getattr(self.defaults, attr)
            except AttributeError:
                raise AttributeError, u'settings object has no attribute "%s"' % attr


class defaults(object):
    FIREWALL_LOGGING = False # Logging is off by default
    FIREWALL_REFRESH = datetime.timedelta(seconds=60) # Not implemented yet
    FIREWALL_REALM = 'Firewall' # Used when prompting for Basic Auth

settings = SettingsProxy(django_settings, defaults)
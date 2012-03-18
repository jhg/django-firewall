from django.db import models
from django.utils.translation import ugettext_lazy as _
import ipaddr
import datetime

class RuleManager(models.Manager):
    def by_ip(self, ip_address, request):
        for rule in self.active_rules():
            if rule.applys(ip_address, request):
                return rule
        return None
    
    def active_rules(self):
        now = datetime.datetime.now()
        queryset = self.filter(is_active=True)
        return queryset
    
    def next_position(self):
        if self.count():
            return self.order_by('-position')[0].position + 1
        return 0
        
class Rule(models.Model):
    RULES = (
           ('ACCEPT', _('Accept')),
           ('REJECT', _('Reject (403)')),
           ('REDIRECT', _('Redirect (302)')),
           ('AUTH', _('Require Auth')),
           ('404', _('404 - Not Found')),
           )
    name = models.CharField(default=_('New rule'), max_length=255, null=True, blank=True,
        help_text=_('Some to remember this rule by.'), )
    
    source = models.CharField(max_length=39, help_text=_("'127.0.0.1', '10.0.0.1', 'private', 'public', 'all'. 10.0.*.* does not work."))
    source_range_end = models.CharField(max_length=39, null=True, blank=True)
    
    action = models.CharField(max_length=20, choices=RULES, default='ACCEPT')
    is_active = models.BooleanField(default=False,)
    
    start_on = models.DateTimeField(null=True, blank=True,)
    stop_on = models.DateTimeField(null=True, blank=True,)
    blocked_paths = models.CharField(max_length=200, null=True, blank=True,
        help_text=_('A comma separated list of paths that will be blocked. (e.g. /beta, /vip/only)'))
    redirect_to_url = models.URLField(u'Redirect to URL', null=True, blank=True,
        help_text=_('Where to redirect unauthorized visitors.'
            ' Can be relative (/home) or fully qualified (http://google.com)'))
    
    username = models.CharField(default='admin', max_length=255, null=True, blank=True,help_text=_("If you select 'Require Auth' the username and password fields will be required"))
    password = models.CharField(default='hackme', max_length=255, null=True, blank=True,)
    
    position = models.PositiveIntegerField()
    
    objects = RuleManager()
    
    """
    This is kinda the thingy method that does all the stuff
    """
    def applys(self, ip_address, request):
        
        # Must be an active rule, double check
        if not self.is_active:
            return False
        
        # path
        if self.blocked_paths:
            match = False
            for path in self.blocked_paths.split(','):
                if request.path.startswith(path.trim(' ')):
                    match = True
            if not match:
                return False
            
        # start and stop
        now = datetime.datetime.now()
        if self.start_on and self.stop_on and (self.start_on > now or self.stop_on < now):
            return False
        
        # start
        if self.start_on and self.start_on > now:
            return False
        
        # stop
        if self.stop_on and self.stop_on < now:
            return False
        
        # check range
        if self.source.upper() == 'ALL':
            return True
        
        # private
        if self.source.upper() == 'PRIVATE' and ip_address.is_private():
            return True
        
        #public
        if self.source.upper() == 'PUBLIC' and not ip_address.is_private():
            return True
        
        # exact ip match
        try:
            source = ipaddr.IPAddress(self.source)
            if ip_address == source:
                return True
        except:
            return False
        
        # range
        if self.source_range_end:
            try:
                source_range_end = ipaddr.IPAddress(self.source_range_end)
                if ip_address > source and ip_address < source_range_end:
                    return True
            except:
                return False
            
        return False
    
    def save(self, *args, **kwargs):
        
        model = self.__class__
        
        if self.position is None:
            # Append
            try:
                last = model.objects.order_by('-position')[0]
                self.position = last.position + 1
            except IndexError:
                # First row
                self.position = 0
        
        super(Rule, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['position', 'is_active']
        permissions = (
            ('firewall_by_pass', 'User can by pass all firewall rules.'),
        )
    
    def __unicode__(self):
        return self.action
    
class Log(models.Model):
    METHODS = (
               ('GET', 'Get'),
               ('POST', 'POST'),
               )
    passed_firewall = models.BooleanField()
    ip = models.IPAddressField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=4, default='GET')
    path = models.TextField()
    http_version = models.CharField(max_length=20, blank=True)
    response_status_code = models.IntegerField(default=200)
    client = models.CharField(max_length=255)
    
    @staticmethod
    def create(request, response, passed_firewall):
        l = Log()
        l.passed_firewall = passed_firewall
        l.ip = request.META.get('REMOTE_ADDR', None)
        if request.POST:
            l.method = 'POST'
        l.path = request.path
        l.http_version = request.META.get('SERVER_PROTOCOL', None)[:20]
        if response is not None:
            l.response_status_code = response.status_code
        l.client = request.META.get('HTTP_USER_AGENT', 'Not provided')[:255]
        l.save()
        return l

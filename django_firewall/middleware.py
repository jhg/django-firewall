from django.http import HttpResponseRedirect, HttpResponse

from models import Rule, Log
from conf import settings
import ipaddr

import datetime
import base64

class FirewallMiddleware():
    
    def process_request(self, request):
        
        if request.user.is_authenticated() and request.user.is_active and request.user.has_perm('django_firewall.firewall_by_pass'):
            return None
        
        try:
            ip_address = ipaddr.IPAddress(request.META.get('REMOTE_ADDR'))
            
            rule = Rule.objects.by_ip(ip_address, request)
            
            # 301
            if rule and rule.action == 'AUTH' and self.valid_auth_request(request, rule):
                return self.log(request, None)
            
            actions = {
                'ACCEPT': None,
                'REJECT': self.create_response(403, 'Forbidden'),
                'AUTH': self.create_response(401),
                '404': self.create_response(404, 'File not found'),
            }
            
            return self.log(request, actions.get(rule.action, None))
        except AttributeError:
            return self.log(request, None)
    
    def create_response(self, status_code, text=''):
        response = HttpResponse(text, content_type="text/html")
        response.status_code = status_code
        if status_code == 401:
            response['WWW-Authenticate'] = 'Basic realm="%s"' % settings.FIREWALL_REALM
        return response
    
    
    def log(self, request, response):
        if settings.FIREWALL_LOGGING:
            Log.create(request, response, True if response is None else False)
        return response
        #return None
    
    def valid_auth_request(self, request, rule):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                # NOTE: We are only support basic authentication for now.
                #
                if auth[0].lower() == "basic":
                    username, password = base64.b64decode(auth[1]).split(':')
                    if username == rule.username and password == rule.password:
                        return True
        return False

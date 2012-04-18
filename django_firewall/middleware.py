from django.http import HttpResponseRedirect, HttpResponse

from models import Rule, Log
from conf import settings
import ipaddr

import datetime
import base64

class FirewallMiddleware():
    
    def process_response(self, request, response):
        Log.create(request, response)
        return response
    
    def process_request(self, request):
        
        if request.user.is_authenticated() and request.user.is_active and request.user.has_perm('django_firewall.firewall_by_pass'):
            return None
        
        try:
            ip_address = ipaddr.IPAddress(request.META.get('REMOTE_ADDR'))
            
            rule = Rule.objects.by_ip(ip_address, request)
            
            # 301
            if rule and rule.action == 'AUTH' and self.valid_auth_request(request, rule):
                return None
            
            actions = {
                'ACCEPT': [200],
                'REJECT': [403, 'Forbidden'],
                'AUTH': [401],
                '404': [404, 'File not found'],
            }
            
            return self.create_response(*actions.get(rule.action, None))
        except AttributeError:
            return None
    
    def create_response(self, status_code, text=''):
        if status_code == 200:
            return None
        
        response = HttpResponse(text, content_type="text/html")
        response.status_code = status_code
        if status_code == 401:
            response['WWW-Authenticate'] = 'Basic realm="%s"' % settings.FIREWALL_REALM
        return response
    
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

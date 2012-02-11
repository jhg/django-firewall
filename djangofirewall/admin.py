from django.contrib import admin
from djangofirewall.models import Rule, Log
from djangofirewall.forms import RuleForm
from django.conf import settings

class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'action', 'source', 'source_range_end', 'position')
    list_filter = ('is_active', 'action',)
    list_editable = ('is_active', 'position', )
    
    form = RuleForm
    
    class Meta:
        models = Rule
        
    class Media:
        js = (
            settings.STATIC_URL + 'firewall/js/jquery-1.7.1.min.js',
            settings.STATIC_URL + 'firewall/js/jquery-ui-1.8.17.custom.min.js',
            settings.STATIC_URL + 'firewall/js/menu-sort.js',
        )

class RuleInline(admin.StackedInline):
    model = Rule

class LogAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'passed_firewall', 'method', 'response_status_code', 'ip',  'path', 'client',)
    list_filter = ('passed_firewall', 'response_status_code', 'method',)
    list_per_page = 50

admin.site.register(Rule, RuleAdmin)
admin.site.register(Log, LogAdmin)




from django.contrib import admin
from models import Rule, Log
from forms import RuleForm

class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'action', 'source', 'source_range_end', 'position')
    list_filter = ('is_active', 'action',)
    list_editable = ('is_active', 'position', )
    list_per_page = 50
    
    form = RuleForm
    
    class Meta:
        models = Rule

class LogAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'passed_firewall', 'method', 'response_status_code', 'ip',  'path', 'client',)
    list_filter = ('passed_firewall', 'response_status_code', 'method',)
    list_per_page = 50

admin.site.register(Rule, RuleAdmin)
admin.site.register(Log, LogAdmin)




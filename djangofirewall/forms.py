from django.utils.translation import ugettext_lazy as _
from django import forms
from djangofirewall.models import Rule

class RuleForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)
        
        if self.data.get('action', '') == 'AUTH':
            self.fields['username'].required = True
            self.fields['password'].required = True
            self.full_clean()
            
        if self.data.get('action', '') == 'REDIRECT':
            self.fields['redirect_to_url'].required = True
            self.full_clean()
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.fields['username'].required and not username:
            raise forms.ValidationError(_('This field is required.'))
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if self.fields['password'].required and not password:
            raise forms.ValidationError(_('This field is required.'))
        return password
    
    def clean_redirect_to_url(self):
        redirect_to_url = self.cleaned_data.get('redirect_to_url')
        if self.fields['redirect_to_url'].required and not redirect_to_url:
            raise forms.ValidationError(_('This field is required.'))
        return redirect_to_url
    
    """
    I don't think this is needed any more... rules can start and stop when ever they like
    
    def clean_start_on(self):
        start_on = self.cleaned_data['start_on']
        is_active = self.cleaned_data.get('is_active', '')
        if is_active:
            try:
                Rule.objects.get(is_active=True,
                    start_on__lte=start_on, stop_on__gte=start_on)
                raise forms.ValidationError("There's already an active Firewall that"
                    " conflicts with this Firewall's start_on date/time.")
            except Rule.DoesNotExist:
                pass
        return start_on
    
    def clean_stop_on(self):
        stop_on = self.cleaned_data['stop_on']
        is_active = self.cleaned_data.get('is_active', '')
        if is_active:
            try:
                Rule.objects.get(is_active=True,
                    start_on__lte=stop_on, stop_on__gte=stop_on)
                raise forms.ValidationError("There's already an active Firewall that"
                    " conflicts with this Firewall's stop_on date/time.")
            except Rule.DoesNotExist:
                pass
        return stop_on
    """
    
    class Meta:
        model = Rule
        exclude = ['position']
# coding=utf-8
from django import forms
from django.forms import ModelForm
from deaspo.models import Project, Product, Plan, ProductWebOrder

class WebOrderForm(ModelForm):
    class Meta:
        model = ProductWebOrder
        fields = {'sites','hosting_plan','backup','wed_design','web_design_name','domain','domain_name','custom_email','custom_email_name','dedicated_inbox','dedicated_inbox_plan','total_price','contact_name','contact_email','contact_no','contact_address','notes','acceptance_terms'}
        widgets = {
            'sites': forms.NumberInput(attrs={'min':"1",'autofocus':"", 'class':"form-control"}),
            'hosting_plan': forms.TextInput(attrs={'readonly': "readonly", 'class':"form-control-static"}),
            'wed_design':forms.CheckboxInput(attrs={'onclick':"return false",'checked':"checked",'value':"1", 'class':"form-control"}),
            'domain': forms.CheckboxInput(attrs={'onclick':"return false",'checked':"checked",'value':"1", 'class':"form-control"}),
            'domain_name':forms.TextInput(attrs={'placeholder':"Name of the website i.e. www.yourcompany.com",'onChange':"setEmail(this.vale)", 'class':"form-control"}),
            'total_price': forms.NumberInput(attrs={'class':"form-control-static"}),
            'custom_email': forms.CheckboxInput(attrs={'onclick':"toggleEmail(this)", 'class':"form-control"}),
            'custom_email_name':forms.TextInput(attrs={'onchange':"fillSample(this.value)",'placeholder':"Your custom email address i.e. name@yourcompany.oom", 'class':"form-control"}),
            'dedicated_inbox': forms.CheckboxInput(attrs={'onclick':"toggleInboxPlans(this)", 'class':"form-control"}),
            'contact_name': forms.TextInput(attrs={'placeholder':"Business/Individual Name", 'class':"form-control"}),
            'contact_email': forms.EmailInput(attrs={'placeholder':"Business/Individual Email", 'class':"form-control"}),
            'contact_no': forms.NumberInput(attrs={'placeholder':"Business/Individual Number", 'class':"form-control"}),
            'contact_address': forms.Textarea(attrs={'placeholder':"Additional Business/Individual Notes", 'class':"form-control"}),
            'acceptance_terms': forms.CheckboxInput(attrs={'class':"form-control"})
        }
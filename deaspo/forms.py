# coding=utf-8
from django import forms
from django.forms import ModelForm
from deaspo.models import Project, Product, Plan, ProductWebOrder, UserProfile,UserNext, Comment, Contact
from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
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


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username':forms.TextInput(attrs={'class':"form-contrl",'placeholder':"preferred username",'name':"username"}),
            'email':forms.EmailInput(attrs={'class':"form-control",'placeholder':"your email address",'name':"email"}),
            'password':forms.PasswordInput(attrs={'placeholder': "Your secret password here",'class':"form-control",'name':"passwd"})

        }

class RegistrationFormWithNext(RegistrationForm):
   next = forms.CharField(max_length=125, required=False)
   def save(self, *args, **kwargs):
      new_user = super(RegistrationFormWithNext, self).save(*args, **kwargs)
      if self.cleaned_data['next']:
         usernext = UserNext()
         usernext.user = new_user
         usernext.next = self.cleaned_data['next']
         usernext.save()
      return new_user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'title','body','user','email','rating'}
        widgets = {
            'title':forms.TextInput(attrs={'class':"form-control animated",'placeholder':"short title for the review",'name':"title"}),
            'user':forms.TextInput(attrs={'class':"form-control",'placeholder':"your name",'name':"user"}),
            'email': forms.EmailInput(attrs={'class': "form-control animated", 'placeholder': "your email address", 'name': "email"}),
            'rating':forms.NumberInput(attrs={'class':"form-control",'type':"hidden",'value':"0",'name':"rating",'id':"ratings-hidden"}),
            'body':forms.Textarea(attrs={'class':"form-control",'placeholder':"Enter your review here..",'id':"new-review",'name':"comment",'cols':"50"})
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = {'cl_email','cl_name','cl_message'}
        widgets = {
            'cl_email':forms.EmailInput(attrs={'class': "form-control", 'placeholder': "E-mail Address", 'name': "email",'id':"email",'required':"required",'autofocus':""}),
            'cl_name':forms.TextInput(attrs={'class': "form-control", 'placeholder': "Name", 'name': "name",'id':"name",'required':"required"}),
            'cl_message':forms.Textarea(attrs={'class':"form-control",'placeholder':"Your Message.",'id':"message",'name':"message",'rows':"5",'required':"required"})
        }
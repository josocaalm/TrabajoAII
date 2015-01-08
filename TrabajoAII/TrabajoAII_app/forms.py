#encoding:utf-8

from django.forms import ModelForm
from django import forms
from TrabajoAII_app.models import *


class SearchUserForm(forms.Form):
    username = forms.CharField()
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ContactForm(forms.Form):
    sender = forms.EmailField()
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
    
class UserForm(ModelForm):
    class Meta:
        model = UserApp
        exclude =('id','last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions','games')
        
class RatingForm(ModelForm):
    class Meta:
        model = Rating
        exclude = ('userApp',)
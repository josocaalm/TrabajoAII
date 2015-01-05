#encoding:utf-8

from django.forms import ModelForm
from django import forms
from TrabajoAII_app.models import *


class SearchUserForm(forms.Form):
    username = forms.CharField()
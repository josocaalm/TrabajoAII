#encoding:utf-8

from django.forms import ModelForm
from django import forms
from Practica10_app.models import *


class SearchUserForm(forms.Form):
    username = forms.CharField()
from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse


class SearchMovieForm(forms.Form):
    keyword = forms.CharField(label='', max_length=256)

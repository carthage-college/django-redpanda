# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError


class SmellTestForm(forms.Form):
    """Data model for the health check app."""
    opt_in = forms.BooleanField(required=False)
    one = forms.BooleanField(required=False)
    two = forms.BooleanField(required=False)
    three = forms.BooleanField(required=False)
    four = forms.BooleanField(required=False)
    five = forms.BooleanField(required=False)
    six = forms.BooleanField(required=False)
    seven = forms.BooleanField(required=False)
    eight = forms.BooleanField(required=False)

# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError


class SmellTestForm(forms.Form):
    """Data model for the health check app."""
    opt_in = forms.BooleanField(required=False)

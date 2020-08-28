# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from redpanda.research.models import SmellStudy


class SmellStudyForm(forms.ModelForm):
    """Data model for the health check app."""

    '''
    one = forms.BooleanField(required=False)
    two = forms.BooleanField(required=False)
    three = forms.BooleanField(required=False)
    four = forms.BooleanField(required=False)
    five = forms.BooleanField(required=False)
    six = forms.BooleanField(required=False)
    seven = forms.BooleanField(required=False)
    eight = forms.BooleanField(required=False)
    '''

    class Meta:
        model = SmellStudy
        exclude = ('created_by', 'created_at')

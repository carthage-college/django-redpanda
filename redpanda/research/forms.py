# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from djtools.fields import BINARY_CHOICES
from redpanda.research.models import Registration
from redpanda.research.models import SmellStudy
from redpanda.research.models import VACCINE_CHOICES


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


class VaccineForm(forms.ModelForm):
    """Data model for the health check app."""
    vaccine = forms.ChoiceField(
        label="Vaccine status",
        choices=VACCINE_CHOICES,
        help_text="""
        Valid reasons for not receiving the vaccine are for: religious beliefs;
        health reasons; or personal conviction. If that is the case, you resolve 
        to continue wearing masks indoors this fall.
        """,
        widget=forms.RadioSelect(),
    )
    vaccine_card_front = forms.FileField(
        label="Vaccine card front",
        help_text="Photo or scan of the front of your COVID-19 vaccine card.",
        required=False,
    )
    vaccine_card_back = forms.FileField(
        label="Vaccine card back",
        help_text="Photo or scan of the back of your COVID-19 vaccine card.",
        required=False,
    )

    class Meta:
        model = Registration
        fields = (
            'vaccine',
            'vaccine_date',
            'vaccine_card_front',
            'vaccine_card_back',
            'vax_rationale',
        )

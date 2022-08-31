# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from djtools.fields import BINARY_CHOICES
from redpanda.research.models import Document
from redpanda.research.models import Registration
from redpanda.research.models import SmellStudy
from redpanda.research.models import VACCINE_CHOICES


class DocumentForm(forms.ModelForm):
    """Data model for vaccine files."""

    class Meta:
        model = Document
        fields = ('phile', 'jab_type', 'jab_date')


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

    class Meta:
        model = Registration
        fields = (
            'vaccine',
            'vax_rationale',
        )

    def clean(self):
        """Verify data based on the user response to vaccine status."""
        cd = self.cleaned_data
        vax = cd.get('vaccine')
        rationale = cd.get('vax_rationale')
        if vax == 'No' and not rationale:
            self.add_error(
                'vax_rationale',
                "Please provide a rationale for not obtaining the vaccine.",
            )
        return cd


class SmellStudyForm(forms.ModelForm):
    """Data model for the health check app."""

    class Meta:
        model = SmellStudy
        exclude = ('created_by', 'created_at')

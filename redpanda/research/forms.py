# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
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

    class Meta:
        model = Registration
        fields = (
            'vaccine',
            'vaccine_date',
            'vaccine_card_front',
            'vax_rationale',
        )

    def __init__(self, *args, **kwargs):
        """Override init method to obtain the request object."""
        self.request = kwargs.pop('request', None)
        super(VaccineForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Verify data based on the user response to vaccine status."""
        user = self.request.user
        perms = user.profile.get_perms()
        faculty = perms.get(settings.FACULTY_GROUP)
        staff = perms.get(settings.STAFF_GROUP)
        cd = self.cleaned_data
        vax = cd.get('vaccine')
        date = cd.get('vaccine_date')
        front = cd.get('vaccine_card_front')
        rationale = cd.get('vax_rationale')
        if vax == 'No' and not rationale:
            self.add_error(
                'vax_rationale',
                "Please provide a rationale for not obtaining the vaccine.",
            )
        elif vax == 'Yes':
            if not date:
                self.add_error(
                    'vaccine_date',
                    "Please provide a date for your first vaccine shot.",
                )
            if not front:
                self.add_error(
                    'vaccine_card_front',
                    "Please upload a photo or scan of the front of your vaccine card.",
                )
        return cd

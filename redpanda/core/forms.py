# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from redpanda.core.models import HealthCheck


class HealthCheckForm(forms.ModelForm):
    """Data model for the health check app."""

    tested_positive = forms.BooleanField(required=False)
    tested_negative = forms.BooleanField(required=False)
    tested_pending = forms.BooleanField(required=False)
    negative = forms.BooleanField(required=False)
    temperature = forms.BooleanField(required=False)
    cough = forms.BooleanField(required=False)
    short_breath = forms.BooleanField(required=False)
    loss_taste_smell = forms.BooleanField(required=False)
    sore_throat = forms.BooleanField(required=False)
    congestion = forms.BooleanField(required=False)
    fatigue = forms.BooleanField(required=False)
    body_aches = forms.BooleanField(required=False)
    headache = forms.BooleanField(required=False)
    nausea = forms.BooleanField(required=False)
    diarrhea = forms.BooleanField(required=False)
    quarantine = forms.BooleanField(required=False)

    class Meta:
        """Information about the data class model."""

        model = HealthCheck
        exclude = ('created_by', 'created_at', 'notification')

    def clean(self):
        cd = super(HealthCheckForm, self).clean()
        if not any(
            cd.get(field, '')
            for field in (
                'tested_positive',
                'tested_negative',
                'tested_pending',
                'negative',
                'temperature',
                'cough',
                'short_breath',
                'loss_taste_smell',
                'sore_throat',
                'congestion',
                'fatigue',
                'body_aches',
                'headache',
                'nausea',
                'diarrhea',
                'quarantine',
            )
        ):
            raise ValidationError("You must check at least one item.")
        return cd

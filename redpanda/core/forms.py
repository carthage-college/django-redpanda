# -*- coding: utf-8 -*-

from django import forms

from redpanda.core.models import HealthCheck


class HealthCheckForm(forms.ModelForm):
    """Data model for the health check app."""

    receive_newsletter = forms.BooleanField()
    positive = forms.BooleanField()
    negative = forms.BooleanField()
    temperature = forms.BooleanField()
    cough = forms.BooleanField()
    short_breath = forms.BooleanField()
    loss_taste_smell = forms.BooleanField()
    sore_throat = forms.BooleanField()
    congestion = forms.BooleanField()
    fatigue = forms.BooleanField()
    body_aches = forms.BooleanField()
    headache = forms.BooleanField()
    nausea = forms.BooleanField()
    diarrhea = forms.BooleanField()
    quarantine = forms.BooleanField()

    class Meta:
        """Information about the data class model."""

        model = HealthCheck
        exclude = ('notification', 'created_at', 'created_by')

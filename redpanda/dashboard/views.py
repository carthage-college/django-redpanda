# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from djimix.decorators.auth import portal_auth_required
from redpanda.core.models import HealthCheck


@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home(request):
    """Dashboard home."""
    return render(
        request,
        'dashboard/home.html',
        {
            'czechs': HealthCheck.objects.all(),
        },
    )


def search(request):
    """Dashboard search."""
    return render(
        request, 'dashboard/search.html', {}
    )

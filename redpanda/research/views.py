# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from djimix.decorators.auth import portal_auth_required
from redpanda.research.forms import SmellTestForm


@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home(request):
    """Smell study form."""
    if request.method == 'POST':
        form = SmellTestForm(request.POST)
        if form.is_valid():
            check = form.save(commit=False)
            check.created_by = request.user
            check.save()
            # messages displayed after submit
            default = "Thank you for participating."
            #tag = 'alert-warning'
            tag = 'alert-success'
            #kind = messages.WARNING
            kind = messages.SUCCESS
            messages.add_message(
                request,
                kind,
                mark_safe('{0}<br>{1}'.format(now, message)),
                extra_tags=tag,
            )
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        form = SmellTestForm()
    return render(request, 'research/home.html', {'form': form})

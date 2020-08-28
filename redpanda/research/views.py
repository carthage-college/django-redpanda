# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from djimix.decorators.auth import portal_auth_required
from redpanda.research.forms import SmellTestForm
from redpanda.research.models import Registration



@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home(request):
    """Smell test form."""
    profile = Registration.objects.get_or_create(
        user=request.user,
    )[0]

    if request.method == 'POST':
        form = SmellTestForm(request.POST)
        if form.is_valid():
            smell = form.save(commit=False)
            smell.created_by = request.user
            smell.save()
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
    return render(
        request, 'research/home.html', {'form': form, 'profile': profile},
    )


@csrf_exempt
@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def opt_in(request):
    if request.is_ajax() and request.method == 'POST':
        pid = request.POST.get('pid')
        profile = Registration.objects.filter(user=request.user).first()
        if profile:
            try:
                profile.opt_in = request.POST.get('opt_in')
                profile.save()
                content = mark_safe(request.POST.get('opt_in'))
            except Exception:
                content = mark_safe('Failed to set opt in value')
        else:
            content = 'Could not fetch user profile'
    else:
        content = "Requires AJAX POST"

    return HttpResponse(content, content_type='text/plain; charset=utf-8')

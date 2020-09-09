# -*- coding: utf-8 -*-

import datetime
import json
import requests

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from djimix.decorators.auth import portal_auth_required
from redpanda.core.forms import HealthCheckForm


@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
    encryption=True,
)
def home(request):
    """Application home."""
    # check in once a day
    # check any and all icons and then submit

    if request.method == 'POST':
        form = HealthCheckForm(request.POST)
        if form.is_valid():
            check = form.save(commit=False)
            check.created_by = request.user
            check.save()
            now = datetime.datetime.now().strftime('%B %d, %Y')
            # messages displayed after submit
            default = """
                Thank you for checking in.<br>Please follow social distancing
                guidelines and check in again tomorrow.
            """
            positive = """
                Thank you for reporting your test results.<br>
                Please consult our
                <a href="https://www.carthage.edu/carthage-covid-19/stay-safe-carthage/symptom-monitoring/">covid resources</a>
                page for more information.<br>
                Check in again tomorrow.
            """
            tested_negative = """
                We have recorded this negative test, so tomorrow please
                <strong>ONLY</strong>
                report your symptoms and isolation plans.
            """
            pending = """
                Thank you for reporting your test results.
                Please consult your health care provider and visit our
                <a href="https://www.carthage.edu/carthage-covid-19/stay-safe-carthage/symptom-monitoring/">covid resources</a>
                page for more information.<br>
            """
            quarantine = """
                Thank you for reporting that you are staying home.<br>
                We will let your professors know.<br>
                Please contact your supervisors directly.<br>
                Check in again tomorrow.
            """
            symptoms = """
                Sorry to hear you are not feeling well.<br>
                Please consult your health care provider and visit our
                <a href="https://www.carthage.edu/carthage-covid-19/stay-safe-carthage/symptom-monitoring/">covid resources</a>
                page for more information.<br>
            """
            tag = 'alert-warning'
            kind = messages.WARNING

            if check.tested_positive:
                message = positive
            elif check.quarantine:
                message = quarantine
            elif check.any_symptoms():
                message = symptoms
            elif check.tested_pending:
                message = pending
                kind = messages.SUCCESS
                tag = 'alert-success'
            elif check.tested_negative:
                message = tested_negative
                kind = messages.SUCCESS
                tag = 'alert-success'
            elif check.negative:
                message = default
                kind = messages.SUCCESS
                tag = 'alert-success'
            else:
                message = default
                kind = messages.SUCCESS
                tag = 'alert-success'

            messages.add_message(
                request,
                kind,
                mark_safe('{0}<br>{1}'.format(now, message)),
                extra_tags=tag,
            )
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        form = HealthCheckForm()
    return render(request, 'home.html', {'form': form})


@csrf_exempt
@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
    group='carthageStaffStatus',
)
def clear_cache(request, ctype='blurb'):
    """Clear the cache for API content."""
    if request.is_ajax() and request.method == 'POST':
        cid = request.POST.get('cid')
        key = 'livewhale_{0}_{1}'.format(ctype, cid)
        cache.delete(key)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        earl = '{0}/live/{1}/{2}@JSON?cache={3}'.format(
            settings.LIVEWHALE_API_URL, ctype, cid, timestamp,
        )
        try:
            response = requests.get(earl, headers={'Cache-Control': 'no-cache'})
            text = json.loads(response.text)
            cache.set(key, text)
            body = mark_safe(text['body'])
        except Exception:
            body = ''
    else:
        body = "Requires AJAX POST"

    return HttpResponse(body, content_type='text/plain; charset=utf-8')

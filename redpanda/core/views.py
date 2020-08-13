# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from djimix.decorators.auth import portal_auth_required
from djtools.utils.mail import send_mail
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
            frum = settings.DEFAULT_FROM_EMAIL
            subject = "[Health Check] {0}, {1} ({2})".format(
                check.created_by.last_name,
                check.created_by.first_name,
                check.created_by.id,
            )
            send_mail(request, [frum], subject, frum, 'email.html', check)
            now = datetime.datetime.now().strftime('%B %d, %Y')
            positive = """
                Thank you for reporting your test results.<br>
                Please consult our
                <a href="https://www.carthage.edu/covid-19/">covid resources</a>
                page for more information.<br>
                Check in again tomorrow.
            """
            negative = """
                Thanks for checking in.<br>Please follow social distancing
                guidelines and check in again tomorrow.
            """
            quarantine = """
                Thank you for reporting that you are staying home.<br>
                We will let your professors know.<br>
                Please contact your supervisors directly.<br>
                Check in again tomorrow.
            """
            symptoms = """
                Sorry to hear you are not feeling well.<br>
                Please consult our
                <a href="https://www.carthage.edu/covid-19/">covid resources</a>
                page for more infomration.<br>
                Check in again tomorrow.
            """
            tag = 'alert-warning'
            kind = messages.WARNING
            if check.negative:
                message = negative
                kind = messages.SUCCESS
                tag = 'alert-success'
            elif check.tested_positive:
                message = positive
            elif check.quarantine:
                message = quarantine
            else:
                message = symptoms

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

# -*- coding: utf-8 -*-

import datetime
import json
import logging
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
from djauth.decorators import portal_auth_required
from redpanda.core.forms import HealthCheckForm
from redpanda.research.forms import DocumentForm
from redpanda.research.forms import VaccineForm
from redpanda.research.models import Registration


REQ_ATTR = settings.REQUIRED_ATTRIBUTE
logger = logging.getLogger('debug_logfile')


@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def vaccine(request):
    """Vaccine verification."""
    user = request.user
    try:
        vaxdoc = user.profile.get_vax()
    except Exception:
        Registration.objects.create(user=user)
        vaxdoc = None
    booster_error = False
    jabs = {}
    if request.method == 'POST':
        form = VaccineForm(
            request.POST,
            instance=user.profile,
            use_required_attribute=REQ_ATTR,
        )
        form_vaxdoc = DocumentForm(
            request.POST,
            request.FILES,
            instance=vaxdoc,
            prefix='vax',
            use_required_attribute=REQ_ATTR,
        )
        if form.is_valid():
            vax = form.save(commit=False)
            if vax.vaccine == 'Yes':
                if form_vaxdoc.is_valid():
                    vax = form.save()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'Thank you for submitting your vaccine status.',
                        extra_tags='alert-success',
                    )
                    doc = form_vaxdoc.save(commit=False)
                    doc.registration = user.profile
                    doc.save()
                    doc.tags.add('Vaccine')
                    for bid in request.POST.getlist('bids[]'):
                        prefix = 'bid{0}'.format(bid)
                        boo = None
                        if int(bid) > 1000:
                            try:
                                boo = Document.objects.get(pk=doc)
                            except Exception:
                                boo = None
                        form_boo = DocumentForm(
                            request.POST,
                            request.FILES,
                            instance=boo,
                            prefix=prefix,
                        )
                        if form_boo.is_valid():
                            booster = form_boo.save(commit=False)
                            booster.registration = user.profile
                            booster.save()
                            booster.tags.add('Booster')
                        else:
                            booster_error = True
                            jabs[bid] = form_boo
                    if booster_error:
                        # this first message will only display for first time users.
                        if vax.booster_due()['due'] or user.profile.get_boosters():
                            message = """
                                There was a problem with one of your booster uploads.
                                Please submit your booster again.
                            """
                        else:
                            message = 'Your booster information is due after {0}.'.format(
                                vax.booster_due()['date'],
                            )
                        messages.add_message(
                            request,
                            messages.WARNING,
                            message,
                            extra_tags='alert-warning',
                        )
                else:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        'Please upload a photo of your vaccine card.',
                        extra_tags='alert-warning',
                    )
    else:
        form = VaccineForm(
            instance=user.profile,
            use_required_attribute=REQ_ATTR,
        )
        form_vaxdoc = DocumentForm(
            instance=vaxdoc,
            prefix='vax',
            use_required_attribute=REQ_ATTR,
        )
    facstaff = False
    perms = user.profile.get_perms()
    if perms.get(settings.FACULTY_GROUP) or perms.get(settings.STAFF_GROUP):
        facstaff = True
    return render(
        request,
        'vaccine.html',
        {
            'form': form,
            'form_vaxdoc': form_vaxdoc,
            'jabs': jabs,
            'facstaff': facstaff,
            'vax_types':  ['Pfizer', 'Moderna', 'Johnson & Johnson'],
        },
    )


@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def health_check(request):
    """Daily health check."""
    # check in once a day
    # check any and all icons and then submit
    user = request.user
    if request.method == 'POST' or request.GET.get('negative'):
        if request.method == 'POST':
            form = HealthCheckForm(request.POST)
        else:
            form = HealthCheckForm(request.GET)
        if form.is_valid():
            check = form.save(commit=False)
            check.created_by = user
            check.save()
            # mobile phone reminders for health check
            if request.POST.get('mobile'):
                user.profile.mobile = True
            elif request.method == "POST":
                user.profile.mobile = False
            # vaccination status
            if request.POST.get('vaccine'):
                user.profile.vaccine = True
            elif request.method == "POST":
                if not user.profile.vaccine:
                    user.profile.vaccine = False
            user.profile.save()
            now = datetime.datetime.now().strftime('%B %d, %Y')
            # messages displayed after submit
            default = """
                Thank you for checking in and honoring your #StaySafeCarthage
                pledge. Please check in again tomorrow.
            """
            positive = """
                The CDC advises that you <strong>seek emergency medical care
                immediately</strong. if you experience trouble breathing,
                persistent pain or pressure in the chest, new confusion,
                inability to wake or stay awake, bluish lips or face, or other
                symptoms that are severe or concerning to you. Get well soon!
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
                CDC guidelines: Get tested if you have symptoms of COVID-19,
                have had close contact (within 6 feet for a total of 15 minutes
                or more) with someone with confirmed COVID-19, or have taken
                part in activities that put you at higher risk due to lack of
                social distancing.
            """
            symptoms = """
                Please get tested/report results and get well soon!
                The CDC advises that you <strong>seek emergency medical care
                immediately</strong>if you experience trouble breathing,
                persistent pain or pressure in the chest, new confusion,
                inability to wake or stay awake, bluish lips or face,
                or other symptoms that are severe or concerning to you.
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
            return HttpResponseRedirect(reverse_lazy('health_check'))
    else:
        form = HealthCheckForm()

    facstaff = False
    perms = user.profile.get_perms()
    if perms.get(settings.FACULTY_GROUP) or perms.get(settings.STAFF_GROUP):
        facstaff = True
    return render(
        request,
        'health_check.html',
        {'form': form, 'facstaff': facstaff, 'ens': None},
    )


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

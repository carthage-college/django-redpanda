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
from redpanda.research.forms import SmellStudyForm
from redpanda.research.models import Registration, SmellStudyInquiry


@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home(request):
    """Smell test form."""
    profile = Registration.objects.get_or_create(
        user=request.user,
    )[0]
    if request.method == 'GET' and request.GET.get('uuid'):
        uuid = uuid=request.GET['uuid']
        inquiry = SmellStudyInquiry.objects.create(
            created_by=request.user, uuid=uuid,
        )
        return HttpResponseRedirect(
            '{0}{1}'.format(settings.REDPANDA_SURVEY_FORM, uuid),
        )
    elif request.method == 'POST':
        # messages displayed after submit
        base = '<p class="mt-4 p-2 alert" id="lossSmell">{message}</p>'.format
        message = base(message="Thank you for participating.")
        form = SmellStudyForm(request.POST)
        if form.is_valid():
            smell = form.save(commit=False)
            smell.created_by = request.user
            smell.save()
            if smell.count() <= 5:
                kind = messages.SUCCESS
                message = base(message='''
                    Having scored five or fewer, you are strongly encouraged to
                    click the "New loss of taste or smell" symptom on the
                    <a href="https://clear.carthage.edu/">
                      daily health-check app</a>.
                    </p>
                ''')
            messages.add_message(
                request,
                messages.SUCCESS,
                mark_safe(message),
                extra_tags='alert-success',
            )
            return HttpResponseRedirect(reverse_lazy('research_home'))
    else:
        form = SmellStudyForm()
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

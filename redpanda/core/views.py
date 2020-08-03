# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from djimix.decorators.auth import portal_auth_required
from redpanda.core.forms import HealthCheckForm


#@portal_auth_required(
    #session_var='REDPANDA_AUTH',
    #redirect_url=reverse_lazy('access_denied'),
#)
def home(request):
    """Application home."""
    # check in once a day
    # check any and all icons and then submit
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

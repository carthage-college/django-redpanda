# -*- coding: utf-8 -*-

"""URLs for all views."""

import os

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models.query import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from djimix.core.database import get_connection
from djimix.core.database import xsql
from djimix.decorators.auth import portal_auth_required
from djtools.utils.users import in_group
from djtools.fields import TODAY
from redpanda.core.models import HealthCheck
from redpanda.core.utils import get_coach

from datetime import datetime
from datetime import timedelta



@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home(request):
    """Dashboard home."""
    user = request.user
    faculty = in_group(user, settings.FACULTY_GROUP)
    admins = in_group(user, settings.ADMIN_GROUP)
    coach = get_coach(user.id)
    students = []
    czechs = None
    if admins or faculty or coach:
        date_start = request.POST.get('date_start')
        if not date_start:
            date_start = TODAY - timedelta(days=1)
        else:
            date_start = datetime.strptime(date_start, '%Y-%m-%d').date()

        date_end = request.POST.get('date_end')
        if not date_end:
            date_end = TODAY + timedelta(days=1)
        else:
            date_end = datetime.strptime(date_end, '%Y-%m-%d').date() + timedelta(days=1)
        '''
        date_end = request.POST.get(
            #'date_end', TODAY + timedelta(days=1)
            'date_end', TODAY
        ) + timedelta(days=2)
        date_end = request.POST.get('date_end', TODAY)
        '''
        if admins:
            czechs = HealthCheck.objects.filter(
                created_at__range=(date_start, date_end)
            ).order_by('-created_at')
            #czechs = HealthCheck.objects.filter(
            #    Q(created_at__gte=date_start) & Q(created_at__lte=date_end)
            #).order_by('-created_at')

        else:
            if coach:
                phile = os.path.join(
                    settings.BASE_DIR, 'sql/students_coach.sql',
                )
            else:
                phile = os.path.join(
                    settings.BASE_DIR, 'sql/students_faculty.sql',
                )
            with open(phile) as incantation:
                sql = incantation.read()
                sql = sql.replace('{CID}', str(user.id))
            with get_connection() as connection:
                roster = xsql(sql, connection).fetchall()
            for ros in roster:
                students.append(
                    {
                        'roster': ros,
                        'czechs': HealthCheck.objects.filter(
                            created_by__id=ros.id,
                        ).filter(created_at__range=(date_start, date_end)),
                    },
                )

        return render(
            request,
            'dashboard/home.html',
            {
                'admins': admins,
                'coach': coach,
                'faculty': faculty,
                'czechs': czechs,
                'students': students,
                'date_start': date_start,
                'date_end': date_end - timedelta(days=1),
            },
        )
    else:
        return HttpResponseRedirect(reverse_lazy('home'))


def search(request):
    """Dashboard search."""
    return render(
        request, 'dashboard/search.html', {}
    )

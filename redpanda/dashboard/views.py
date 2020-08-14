# -*- coding: utf-8 -*-

"""URLs for all views."""

import os

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from djimix.core.database import get_connection
from djimix.core.database import xsql
from djimix.decorators.auth import portal_auth_required
from djtools.utils.users import in_group
from redpanda.core.models import HealthCheck


@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home(request):
    """Dashboard home."""
    user = request.user
    faculty = in_group(user, settings.FACULTY_GROUP)
    admins = in_group(user, settings.ADMIN_GROUP)
    students = []
    czechs = None
    if faculty or admins:
        if admins:
            czechs = HealthCheck.objects.all().order_by('-created_at')
        else:
            if request.coaches:
                phile = os.path.join(settings.BASE_DIR, 'sql/students_coaches.sql')
            else:
                phile = os.path.join(settings.BASE_DIR, 'sql/students_faculty.sql')
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
                            created_by__id=ros.student_id,
                        ),
                    },
                )

        return render(
            request,
            'dashboard/home.html',
            {
                'admins': admins,
                'faculty': faculty,
                'czechs': czechs,
                'students': students,
            },
        )
    else:
        return HttpResponseRedirect(reverse_lazy('home'))


def search(request):
    """Dashboard search."""
    return render(
        request, 'dashboard/search.html', {}
    )

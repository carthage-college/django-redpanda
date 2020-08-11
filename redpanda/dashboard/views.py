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
    if faculty:
        phile = os.path.join(settings.BASE_DIR, 'sql/students_faculty.sql')
        with open(phile) as incantation:
            sql = incantation.read()
            sql = sql.replace('CID', str(user.id))
        with get_connection() as connection:
            students = xsql(sql, connection).fetchall()
        cids = []
        for student in students:
            cids.append(student.student_id)
        czechs = HealthCheck.objects.filter(created_by__id__in=cids)
    else:
        czechs = HealthCheck.objects.all().order_by('-created_at')
    return render(request, 'dashboard/home.html', {'czechs': czechs})


def search(request):
    """Dashboard search."""
    return render(
        request, 'dashboard/search.html', {}
    )

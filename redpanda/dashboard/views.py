# -*- coding: utf-8 -*-

"""URLs for all views."""

import os


from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models.query import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from djimix.core.database import get_connection
from djimix.core.database import xsql
from djimix.decorators.auth import portal_auth_required
from djtools.utils.users import in_group
from djtools.fields import TODAY
from redpanda.core.models import HealthCheck
from redpanda.core.utils import get_coach

from datetime import datetime
from datetime import timedelta


def _get_dates(request):
    today = TODAY
    date_start = request.POST.get('date_start')
    if not date_start:
        date_start = today - timedelta(days=1)
    else:
        date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
    date_end = request.POST.get('date_end')
    if not date_end:
        date_end = today + timedelta(days=1)
    else:
        date_end = datetime.strptime(date_end, '%Y-%m-%d').date() + timedelta(days=1)

    return (date_start, date_end)


@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home(request):
    """Dashboard home."""
    user = request.user
    faculty = in_group(user, settings.FACULTY_GROUP)
    admins = in_group(user, settings.ADMIN_GROUP)
    athletics = in_group(user, settings.ATHLETICS_GROUP)
    coach = get_coach(user.id)
    sport = '666'
    sports = None

    sportsql = os.path.join(settings.BASE_DIR, 'sql/sports_all.sql')
    with open(sportsql) as incantation:
        with get_connection() as connection:
            sports = xsql(incantation.read(), connection).fetchall()
    # simple protection against sql injection
    for spor in sports:
        if spor[0] == request.POST.get('sport'):
            sport = spor[0]
            break

    date_start, date_end = _get_dates(request)

    return render(
        request,
        'dashboard/home.html',
        {
            'admins': admins,
            'athletics': athletics,
            'coach': coach,
            'faculty': faculty,
            'sport': sport,
            'sports': sports,
            'date_start': date_start,
            'date_end': date_end - timedelta(days=1),
        },
    )


@csrf_exempt
@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home_ajax(request):
    """ajax response for dashboard home."""
    user = request.user
    faculty = in_group(user, settings.FACULTY_GROUP)
    admins = in_group(user, settings.ADMIN_GROUP)
    athletics = in_group(user, settings.ATHLETICS_GROUP)
    coach = get_coach(user.id)
    students = []
    czechs = None
    post = request.POST
    # draw counter
    draw = int(post.get('draw', 0))
    # paging first record indicator.
    start = int(post.get('start', 0))
    # number of records that the table can display in the current draw
    length = int(post.get('length', 100))
    # search box data
    search = post.get('search[value]')
    # order by
    order = int(post.get('order[0][column]'))
    # direction
    dirx = post.get('order[0][dir]')
    cols = {
        0: 'serial',
        1: 'ci',
        2: 'ip',
        3: 'env',
        4: 'subenv',
        5: 'cpu',
        6: 'mem',
        7: 'disk',
        8: 'os',
        9: 'dsc',
        10: 'pd',
        11: 'status',
        12: 'machine_type'
    }
    order_by = cols.get(order) if dir == 'desc' else '-' + cols.get(order)
    if admins or faculty or athletics or coach:
        date_start, date_end = _get_dates(request)
        if admins:
            records_total = HealthCheck.objects.filter(
                created_at__range=(date_start, date_end)
            ).order_by('-created_at').count()
            all_czechs = HealthCheck.objects.filter(
                created_at__range=(date_start, date_end)
            ).order_by('-created_at')
            records_filtered = records_total
            paginator = Paginator(all_czechs, length)
            try:
                object_list = paginator.page(draw).object_list
            except PageNotAnInteger:
                object_list = paginator.page(draw).object_list
            except EmptyPage:
                object_list = paginator.page(paginator.num_pages).object_list

            data = []
            for czech in object_list:
                full_name = '{0}, {1}'.format(
                    czech.created_by.last_name, czech.created_by.first_name,
                )
                if czech.created_by.groups.filter(name=settings.FACULTY_GROUP).exists():
                    group = 'Faculty'
                elif czech.created_by.groups.filter(name=settings.STUDENT_GROUP).exists():
                    group = 'Student'
                else:
                    group = 'Staff'

                data.append({
                    'email': czech.created_by.email,
                    'full_name': full_name,
                    'cid': czech.created_by.id,
                    'created_at': czech.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'group': group,
                    'tested_positive': czech.tested_positive,
                    'tested_negative': czech.tested_negative,
                    'tested_pending': czech.tested_pending,
                    'negative': czech.negative,
                    'temperature': czech.temperature,
                    'cough': czech.cough,
                    'short_breath': czech.short_breath,
                    'loss_taste_smell': czech.loss_taste_smell,
                    'sore_throat': czech.sore_throat,
                    'congestion': czech.congestion,
                    'fatigue': czech.fatigue,
                    'body_aches': czech.body_aches,
                    'headache': czech.headache,
                    'nausea': czech.nausea,
                    'diarrhea': czech.diarrhea,
                    'quarantine': czech.quarantine,
                })
        else:
            if athletics:
                date = settings.START_DATE
                if date.month < settings.SPORTS_MONTH:
                    year = date.year
                else:
                    year = date.year + 1
                phile = os.path.join(
                    settings.BASE_DIR, 'sql/students_sport.sql',
                )
            elif coach:
                phile = os.path.join(
                    settings.BASE_DIR, 'sql/students_coach.sql',
                )
            else:
                phile = os.path.join(
                    settings.BASE_DIR, 'sql/students_faculty.sql',
                )
            with open(phile) as incantation:
                sql = incantation.read()
                if athletics:
                    sql = sql.replace('{YEAR}', str(year)).replace('{SPORT}', sport)
                else:
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
        return JsonResponse(
            {
                'draw': draw,
                'recordsTotal': records_total,
                'recordsFiltered': records_filtered,
                'data': data,
            },
            safe=False,
        )
    else:
        return HttpResponseRedirect(reverse_lazy('home'))


@portal_auth_required(
    session_var='REDPANDA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def research(request):
    """Dashboard for smell study."""
    user = request.user
    admins = in_group(user, settings.ADMIN_GROUP)
    study = in_group(user, settings.RESEARCH_GROUP)
    date_start, date_end = _get_dates(request)

    if admins or study:
        czechs = HealthCheck.objects.filter(
            created_at__range=(date_start, date_end)
        ).filter(
            created_by__profile__opt_in='Yes',
        ).order_by('-created_at')
        response =  render(
            request,
            'dashboard/research.html',
            {'czechs': czechs, 'research': study},
        )
    else:
        response = HttpResponseRedirect(reverse_lazy('home'))
    return response

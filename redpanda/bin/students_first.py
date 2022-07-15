#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redpanda.settings.shell')

# required if using django models
import django
django.setup()

from django.conf import settings
from djimix.core.database import get_connection
from djimix.core.database import xsql
from redpanda.research.models import Registration


def main():
    """Obtain first year students and report on vax status."""
    # fetch our students
    phile = os.path.join(settings.BASE_DIR, 'sql/students_first_year.sql')
    with open(phile) as incantation:
        sql = incantation.read()
    with get_connection() as connection:
        students = xsql(sql, connection).fetchall()
    sids = []
    for student in students:
        sids.append(student.id)
    profiles = Registration.objects.filter(user__id__in=sids)
    for prof in profiles:
        print("{0}|{1}|{2}|{3}".format(
            prof.user.id, prof.user.last_name, prof.user.first_name, prof.vaccine,
        ))


if __name__ == '__main__':

    sys.exit(main())

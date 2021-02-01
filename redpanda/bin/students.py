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
from djimix.core.encryption import encrypt
from djtools.utils.mail import send_mail


def main():
    """Send students notification to complete daily health check."""
    request = None
    frum = settings.DEFAULT_FROM_EMAIL
    subject = "[Health Check] Daily Reminder"
    # fetch our students
    phile = os.path.join(settings.BASE_DIR, 'sql/students.sql')
    with open(phile) as incantation:
        sql = incantation.read()
    with get_connection() as connection:
        students = xsql(sql, connection).fetchall()

    # fetch our UUID
    mobi = 0
    mail = 0
    with get_connection(settings.MSSQL_EARL, encoding=False) as mssql_cnxn:
        for student in students:
            sql = "SELECT * FROM fwk_user WHERE HostID like '%{}'".format(student.id)
            row = xsql(sql, mssql_cnxn).fetchone()
            if row:
                earl = 'https://{0}{1}?uid={2}'.format(
                    settings.SERVER_URL,
                    settings.ROOT_URL,
                    encrypt(row[0]),
                )
                # send an SMS or an email
                if student.mobile:
                    print(student.mobile)
                    mobi += 1
                else:
                    email = student.email
                    mail += 1
                    print(email)
                    context_data = {'earl': earl, 'peep': student}
                    '''
                    send_mail(
                        request,
                        [email],
                        subject,
                        frum,
                        'email_reminder.html',
                        context_data,
                    )
                    '''
    print(mobi)
    print(mail)


if __name__ == '__main__':

    sys.exit(main())

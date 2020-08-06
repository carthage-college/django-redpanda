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
from djimix.people.utils import get_peeps
from djimix.core.encryption import encrypt
from djtools.utils.mail import send_mail


def main():
    """Main function description."""
    request = None
    frum = settings.DEFAULT_FROM_EMAIL
    subject = "[Health Check] Daily Reminder"
    for counter, peep in enumerate(get_peeps('facstaff')):
        email = peep['email']
        sql = "SELECT * FROM fwk_user WHERE HostID like '%{}'".format(peep['cid'])
        connection = get_connection(settings.MSSQL_EARL, encoding=False)
        with connection:
            results = xsql(sql, connection)
            row = results.fetchone()
            if row:
                earl = 'https://{0}{1}?uid={2}'.format(
                    settings.SERVER_URL,
                    settings.ROOT_URL,
                    encrypt(row[0]),
                )
                context_data = {'earl': earl, 'peep': peep}
                send_mail(
                    request,
                    [email],
                    subject,
                    frum,
                    'email_reminder.html',
                    context_data,
                )


if __name__ == '__main__':

    sys.exit(main())

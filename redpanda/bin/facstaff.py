# -*- coding: utf-8 -*-

import json
import os
import requests
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
    """Send fac/staff notification to complete daily health check."""
    request = None
    frum = settings.DEFAULT_FROM_EMAIL
    subject = "[Health Check] Daily Reminder"

    sql = 'SELECT * FROM provisioning_vw WHERE id in {0}'.format(
        settings.REDPANDA_TEST_CIDS,
    )
    print(sql)
    with get_connection() as connection:
        peeps = xsql(sql, connection).fetchall()
    #peeps = get_peeps('facstaff')
    for peep in peeps:
        #email = peep['email']
        email = '{0}@carthage.edu'.format(peep[3])
        #sql = "SELECT * FROM fwk_user WHERE HostID like '%{}'".format(peep['cid'])
        sql = "SELECT * FROM fwk_user WHERE HostID like '%{}'".format(peep[0])
        with get_connection(settings.MSSQL_EARL, encoding=False) as connection:
            results = xsql(sql, connection)
            row = results.fetchone()
            if row:

                earl = 'https://{0}{1}{2}?uid={3}'.format(
                    settings.REDPANDA_SERVER_URL,
                    settings.REDPANDA_ROOT_URL,
                    settings.REDPANDA_SHORT_URL_API,
                    row[0],
                )
                print(earl)
                response = requests.get(earl)
                jason_data = json.loads(response.text)
                earl = jason_data['lynx']
                print(earl)
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

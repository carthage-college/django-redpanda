# -*- coding: utf-8 -*-

import json
import logging
import os
import requests
import sys

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redpanda.settings.shell')

# required if using django models
import django
django.setup()

from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader
from djimix.core.database import get_connection
from djimix.core.database import xsql
from djimix.people.utils import get_peeps
from djimix.core.encryption import encrypt
from djtools.utils.mail import send_mail

# informix environment
os.environ['INFORMIXSERVER'] = settings.INFORMIXSERVER
os.environ['DBSERVERNAME'] = settings.DBSERVERNAME
os.environ['INFORMIXDIR'] = settings.INFORMIXDIR
os.environ['ODBCINI'] = settings.ODBCINI
os.environ['ONCONFIG'] = settings.ONCONFIG
os.environ['INFORMIXSQLHOSTS'] = settings.INFORMIXSQLHOSTS
os.environ['LD_LIBRARY_PATH'] = settings.LD_LIBRARY_PATH
os.environ['LD_RUN_PATH'] = settings.LD_RUN_PATH

logger = logging.getLogger('debug_logfile')


def main():
    """Send fac/staff notification to complete daily health check."""
    request = None
    frum = settings.EMAIL_HOST_USER
    subject = "Daily Health Check Reminder: {sn}, {fn}".format
    peeps = get_peeps('facstaff')
    for peep in peeps:
        email = peep['email']
        sql = "SELECT * FROM fwk_user WHERE HostID like '%{}'".format(peep['cid'])
        print(email)
        print(sql)
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
                context_data = {'earl': earl, 'peep': peep}
                print(context_data)

                # debugging problems with gmail smtp
                headers = {'Reply-To': frum,'From': frum,}
                print(headers)
                template = loader.get_template('email_reminder.html')
                rendered = template.render({'data':context_data,}, request)
                email = EmailMessage(
                    subject(sn=peep['lastname'], fn=peep['firstname']),
                    rendered,
                    frum,
                    [email],
                    headers=headers,
                )
                email.encoding = 'utf-8'
                email.content_subtype = 'html'

                try:
                    email.send(fail_silently=False)
                except Exception as e:
                    logger.debug(e)
                    logger.debug(peep['cid'])

                '''
                send_mail(
                    request,
                    [email],
                    subject,
                    frum,
                    'email_reminder.html',
                    context_data,
                    bcc=[frum],
                )
                '''


if __name__ == '__main__':

    sys.exit(main())

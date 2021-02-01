#! /usr/bin/env python3
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
    subject = "Daily Health Check Reminder"
    to_list = settings.REDPANDA_FACSTAFF_TO_LIST
    earl = 'https://{0}{1}'.format(
        settings.REDPANDA_SERVER_URL,
        settings.REDPANDA_ROOT_URL,
    )
    send_mail(
        request,
        to_list,
        subject,
        frum,
        'email_reminder_list.html',
        {'earl': earl},
        bcc=[frum],
    )


if __name__ == '__main__':

    sys.exit(main())

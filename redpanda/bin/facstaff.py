# -*- coding: utf-8 -*-

import os
import sys

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redpanda.settings.shell')

# required if using django models
import django
django.setup()

from django.conf import settings
from django.core.cache import cache
from django.core.validators import validate_email
from django.urls import reverse_lazy
from djimix.core.database import get_connection
from djimix.core.database import xsql
from djimix.people.utils import get_peeps
from djimix.core.encryption import encrypt

import logging

logger = logging.getLogger('debug_logfile')


def main():
    """Main function description."""
    for peep in get_peeps('facstaff'):
        #print(get_uuid(peep['email']))
        #print(peep['email'])
        email = peep['email']
        sql = "SELECT * FROM fwk_user WHERE HostID like '%{}'".format(peep['cid'])
        connection = get_connection(settings.MSSQL_EARL, encoding=False)
        with connection:
            results = xsql(sql, connection)
            row = results.fetchone()
            if row:
                print(
                    "https://{0}{1}?uid={2}".format(
                        settings.SERVER_URL,
                        settings.ROOT_URL,
                        encrypt(row[0]),
                    ),
                    row[4],
                )


if __name__ == '__main__':

    sys.exit(main())

# -*- coding: utf-8 -*-

"""URLs for all views."""

import os

from django.conf import settings
from djimix.core.database import get_connection
from djimix.core.database import xsql


def get_coach(cid):
    """Obtain an athletics coach based on ID."""
    phile = os.path.join(settings.BASE_DIR, 'sql/coach.sql')
    with open(phile) as incantation:
        sql = incantation.read()
        sql = sql.replace('{CID}', str(cid))
    with get_connection() as connection:
        return xsql(sql, connection).fetchone()

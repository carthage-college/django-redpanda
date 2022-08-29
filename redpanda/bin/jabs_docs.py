#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import django
import os
import sys
import time

django.setup()

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redpanda.settings.shell')

from django.conf import settings
from redpanda.research.models import Document
from redpanda.research.models import Registration


# set up command-line options
desc = "use --test flag to print debug data."

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def _timestamp(instance, field):
    """Obtain the timestamp from the file system."""
    attr = getattr(instance, field, None)
    if attr:
        path = os.path.join(settings.MEDIA_ROOT, attr.name)
        # ctime() does not refer to creation time on *nix systems,
        # but rather the last time the inode data changed: time.ctime(getctime(path))
        # time.gmtime() returns the time in UTC so we use time.localtime()
        ts = datetime.datetime.fromtimestamp(
            time.mktime(time.localtime(os.path.getmtime(path))),
        )
    else:
        ts = None
    return ts


def main():
    """Determine when someone tests positive after loss of smell."""

    reggies = Registration.objects.filter(
        vaccine='Yes',
    ).order_by('created_at')
    for reggie in reggies:
        vax_ts = _timestamp(reggie, 'vaccine_card_front')
        if vax_ts:
            vax = Document.objects.create(
                created_at=vax_ts,
                updated_at=vax_ts,
                registration=reggie,
                phile=reggie.vaccine_card_front,
                jab_date=reggie.vaccine_date,
            )
            vax.tags.add('Vaccine')
        boo_ts = _timestamp(reggie, 'booster_proof')
        if boo_ts:
            boo = Document.objects.create(
                created_at=boo_ts,
                updated_at=boo_ts,
                registration=reggie,
                phile=reggie.booster_proof,
                jab_date=reggie.booster_date,
            )
            boo.tags.add('Booster')
        if test:
            print('{0}|{1}|{2}|{3}|{4}'.format(
                vax_ts,
                reggie.vaccine_card_front,
                reggie.vaccine_date,
                boo_ts,
                reggie.booster_date,
                reggie.booster_proof,
            ))


if __name__ == '__main__':
    args = parser.parse_args()
    test = args.test
    if test:
        print(args)

    sys.exit(main())

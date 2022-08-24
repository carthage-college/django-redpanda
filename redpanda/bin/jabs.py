#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import django
import os
import sys

django.setup()

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redpanda.settings.shell')

from redpanda.research.models import Document
from redpanda.research.models import Registration


# set up command-line options

def main():
    """Determine when someone tests positive after loss of smell."""

    reggies = Registration.objects.filter(
        vaccine='Yes',
    ).order_by('created_at')
    for reggie in reggies:
        print('{0}|{1}|{2}|{3}'.format(
            reggie.vaccine_date,
            reggie.vaccine_card_front,
            reggie.booster_date,
            reggie.booster_proof,
        ))


if __name__ == '__main__':

    sys.exit(main())

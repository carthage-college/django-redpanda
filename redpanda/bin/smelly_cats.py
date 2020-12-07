# -*- coding: utf-8 -*-

import django
import os
import sys

django.setup()

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redpanda.settings.shell')

from redpanda.core.models import HealthCheck


# set up command-line options

def main():
    """Determine when someone tests positive after loss of smell."""

    smelly_cats=[]
    smellloss = HealthCheck.objects.filter(
        loss_taste_smell=True,
    ).order_by('created_at')
    print('Loss of smell date|Positive date')
    for loss in smellloss:
        if loss.created_by.id not in smelly_cats:
            smelly_cats.append(loss.created_by.id)
            positive = HealthCheck.objects.filter(
                created_by=loss.created_by,
            ).filter(tested_positive=True).order_by('created_at').first()
            if positive:
                print('{0}|{1}'.format(
                    loss.created_at,
                    positive.created_at,
                ))
    print(len(smelly_cats))


if __name__ == '__main__':

    sys.exit(main())

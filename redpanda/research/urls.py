# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from redpanda.research import views


urlpatterns = [
    path('opt-in/', view=views.opt_in, name='opt_in'),
    path('', view=views.home, name='research_home'),
]

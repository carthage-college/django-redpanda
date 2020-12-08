# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path

from redpanda.dashboard import views


urlpatterns = [
    path(
        'managers/',
        views.managers, name='dashboard_managers',
    ),
    path(
        'participation/',
        views.participation, name='dashboard_participation',
    ),
    path(
        'research/',
        views.research, name='dashboard_research',
    ),
    path('ajax/', views.home_ajax, name='home_ajax'),
    path('', views.home, name='dashboard'),
]

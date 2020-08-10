# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from redpanda.lynx import views


urlpatterns = [
    path('api/', view=views.api, name='api'),
    path('<str:earl_hash>/', view=views.rewrite, name='rewrite'),
    path('', RedirectView.as_view(url=reverse_lazy('home')), name='lynx'),
]

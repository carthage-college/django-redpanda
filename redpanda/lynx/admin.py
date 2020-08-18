# -*- coding: utf-8 -*-

"""Admin classes for data models."""

from django.contrib import admin
from redpanda.lynx.models import URL


class URLAdmin(admin.ModelAdmin):
    """URL shortener admin class."""

    list_display = (
        'earl_hash',
        'clicks',
        'created_at',
        'earl_full',
    )
    list_per_page = 500
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


admin.site.register(URL, URLAdmin)

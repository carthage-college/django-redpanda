# -*- coding: utf-8 -*-

"""Admin classes for data models."""

from django.contrib import admin
from django.db import models
from redpanda.research.models import Registration


class ProfileAdmin(admin.ModelAdmin):
    """Registration user profile admin class."""

    list_display = ('profile_username', 'profile_vaccine', 'profile_firstname')
    #list_editable = ('profile_vaccine',)
    list_per_page = 500
    raw_id_fields = ('user',)

    date_hierarchy = 'created_at'
    readonly_fields = ('user',)
    search_fields = (
        'user__username',
        'user__last_name',
        'user__first_name',
        'user__id',
    )

    def profile_username(self, instance):
        """Return user's username."""
        return instance.user.username
    profile_username.short_description = "username"

    def profile_vaccine(self, instance):
        """Return user's vax status."""
        return instance.user.profile.vaccine
    profile_vaccine.short_description = "vaccine"

    def profile_firstname(self, instance):
        """Return user's given name."""
        return instance.user.first_name
    profile_firstname.short_description = "first name"


admin.site.register(Registration, ProfileAdmin)

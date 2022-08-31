# -*- coding: utf-8 -*-

"""Admin classes for data models."""

from django.contrib import admin
from django.db import models
from redpanda.research.models import Document
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


class DocumentAdmin(admin.ModelAdmin):
    """Document data model admin."""

    list_per_page = 500
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['registration']
    list_display = (
        '__str__',
        'registration',
        'creator_name',
        'created_at',
        'jab_date',
        'phile',
        'all_tags',
    )
    search_fields = (
        'registration__user__username',
        'registration__user__last_name',
        'registration__user__first_name',
        'registration__user__id',
    )


    def creator_name(self, instance):
        return "{0}, {1}".format(
            instance.registration.user.last_name,
            instance.registration.user.first_name,
        )
    #creator_name.admin_order_field  = 'created_by'
    creator_name.short_description = "Submitted by"

    def all_tags(self, instance):
        return instance.get_tags()
    all_tags.short_description = "Tags"

    def phile(self, instance):
        """Construct display file code for the admin dashboard."""
        icon = mark_safe(
            """
            <a href="{0}">
            <i class="fa fa-check green" aria-hidden="true" title="{1}"></i></a>
            """.format(instance.phile, instance.get_tags()),
        )
        return icon
    phile.allow_tags = True
    phile.short_description = "File"


admin.site.register(Document, DocumentAdmin)
admin.site.register(Registration, ProfileAdmin)

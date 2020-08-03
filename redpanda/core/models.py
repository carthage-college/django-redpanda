# -*- coding: utf-8 -*-

"""Data models."""

from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


class GenericChoice(models.Model):
    """Choices for model and form fields that accept for multiple values."""

    name = models.CharField(max_length=255)
    value = models.CharField(unique=True, max_length=255)
    rank = models.IntegerField(
        verbose_name="Ranking",
        null=True,
        blank=True,
        default=0,
        help_text="A number that determines this object's position in a list.",
    )
    active = models.BooleanField(
        help_text="""
            Do you want the field to be visable on the public submission form?
        """,
        verbose_name="Is active?",
        default=True,
    )
    admin = models.BooleanField(
        verbose_name="Administrative only", default=False,
    )
    tags = TaggableManager(blank=True)

    class Meta:
        """Attributes about the data model and admin options."""

        ordering = ['rank']

    def __str__(self):
        """Default data for display."""
        return self.name


class HealthCheck(models.Model):
    """Data class model for the Health Check app."""

    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name="health_check_created_by",
        editable=False, null=True, blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    positive = models.BooleanField(
        "I've tested positive for COVID-19",
        null=True,
        blank=True,
    )
    negative = models.BooleanField(
        "No Symptoms",
        null=True,
        blank=True,
    )
    temperature = models.BooleanField(
        "Temp ≥ 100.4 F/38.0 C or Chills",
        null=True,
        blank=True,
    )
    cough = models.BooleanField(
        "New Cough",
        null=True,
        blank=True,
    )
    short_breath = models.BooleanField(
        "Shortness of breath",
        null=True,
        blank=True,
    )
    loss_taste_smell = models.BooleanField(
        "New Loss of Taste or Smell",
        null=True,
        blank=True,
    )
    sore_throat = models.BooleanField(
        "Sore throat",
        null=True,
        blank=True,
    )
    congestion = models.BooleanField(
        "Congestion or Runny Nose (excluding seasonal allergies)",
        null=True,
        blank=True,
    )
    fatigue = models.BooleanField(
        "New Unexplained Fatigue",
        null=True,
        blank=True,
    )
    body_aches = models.BooleanField(
        "Muscle or Body Ache",
        null=True,
        blank=True,
    )
    headache = models.BooleanField(
        "New Headache",
        null=True,
        blank=True,
    )
    nausea = models.BooleanField(
        "Nausea or Vomiting",
        null=True,
        blank=True,
    )
    diarrhea = models.BooleanField(
        "Diarrhea",
        null=True,
        blank=True,
    )
    quarantine = models.BooleanField(
        "Self quarantine due to symptoms or suspected COVID exposure",
        null=True,
        blank=True,
    )
    notification = models.BooleanField(
        "Notification sent?",
        null=True,
        blank=True,
    )

    class Meta:
        """Information about the data class model."""
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self):
        """Default data for display."""
        return self.created_by.username

    def get_absolute_url(self):
        """URL for the display view of the data class model."""
        return ('health_check_detail', [self.id])


class Annotation(models.Model):

    health_check = models.ForeignKey(
        HealthCheck,
        related_name='notes',
        on_delete=models.PROTECT,
    )
    created_by = models.ForeignKey(
        User, verbose_name="Created by",
        related_name='note_creator',
        on_delete=models.PROTECT,
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='note_updated',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        "Date Created", auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Date Updated", auto_now=True,
    )
    recipients = models.ManyToManyField(
        User, blank=True,
    )
    body = models.TextField()
    status = models.BooleanField(default=True, verbose_name="Active?")
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        """Default data for display."""
        return "{0}, {1}".format(
            self.created_by.last_name, self.created_by.first_name
        )


class Message(models.Model):
    """Automated message content sent from the system."""

    name = models.CharField(
        max_length=255,
    )
    body = models.TextField(
        help_text="Message content in text/html"
    )
    status = models.BooleanField(default=False, verbose_name="Active?")

# -*- coding: utf-8 -*-

"""Data models."""

from django.db import models
from django.contrib.auth.models import User
from redpanda.core.models import GenericChoice


class SmellStudy(models.Model):
    """Data class model for the smell acuity daily test."""

    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name="smellstudy_created_by",
        editable=False, null=True, blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    affirmative = models.CharField(
        "I could smell all 3 odors in my kit today (if checked: DONE)",
        max_length=8,
    )
    # if user selects 5 or fewer: GO TO THE NURSE)
    item_test = models.CharField(
        verbose_name="""
            I had difficulty smelling 1 or more of my 3 odors today
            and so I completed the 8-item Test again and I had
            the following number correct.
        """,
        max_length=4,
    )


class Registration(models.Model):
    """Data class model for the smell acuity research registration."""

    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name="registration_created_by",
        editable=False, null=True, blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    odor_identification = models.CharField(
        verbose_name="""
            How many items did you answer correctly (out of 8)
            on the odor identification task?
        """,
        max_length=4,
    )
    opt_in = models.BooleanField(
        "I would like to participate in the smell study",
        default=True,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    age = models.CharField(max_length=4)
    biological_sex = models.CharField(max_length=8)
    race = models.ManyToManyField(
        GenericChoice,
        related_name="user_profile_race",
        help_text = 'Check all that apply'
    )
    allergy_symptoms = models.CharField(max_length=4)
    smoking_status = models.CharField(max_length=16)
    medications = models.TextField()
    incorrect_items = models.ManyToManyField(GenericChoice)

    class Meta:
        """Information about the data class model."""
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self):
        """Default data for display."""
        return self.created_by.username

    #def get_absolute_url(self):
        #"""URL for the display view of the data class model."""
        #return ('health_check_detail', [self.id])

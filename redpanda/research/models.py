# -*- coding: utf-8 -*-

"""Data models."""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import FileExtensionValidator
from djtools.fields import BINARY_CHOICES
from djtools.fields.helpers import upload_to_path
from redpanda.core.models import GenericChoice

ALLOWED_IMAGE_EXTENSIONS = (
    'jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG', 'pdf', 'PDF',
)
VACCINE_CHOICES = (
    ('Yes', 'I have been vaccinated.'),
    ('No', 'I have a reason not to be vaccinated.')
)


class SmellStudy(models.Model):
    """Data class model for the smell acuity daily test."""

    created_by = models.ForeignKey(
        User,
        verbose_name='Created by',
        related_name='study',
        editable=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(
        "Date Created", auto_now_add=True,
    )
    one = models.BooleanField()
    two = models.BooleanField()
    three = models.BooleanField()
    four = models.BooleanField()
    five = models.BooleanField()
    six = models.BooleanField()
    seven = models.BooleanField()
    eight = models.BooleanField()

    def count(self):
        smell = 0
        if self.one:
            smell += 1
        if self.two:
            smell += 1
        if self.three:
            smell += 1
        if self.four:
            smell += 1
        if self.five:
            smell += 1
        if self.six:
            smell += 1
        if self.seven:
            smell += 1
        if self.eight:
            smell += 1
        return smell


class SmellStudyInquiry(models.Model):
    """Data class model for the smell acuity daily inquiry form."""
    created_by = models.ForeignKey(
        User,
        verbose_name='Created by',
        related_name='inquiry',
        editable=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(
        "Date Created", auto_now_add=True,
    )
    uuid = models.CharField(max_length=128, null=True, blank=True)


class Registration(models.Model):
    """Data class model for the smell acuity research registration."""
    user = models.OneToOneField(
        User,
        verbose_name='Created by',
        related_name='profile',
        editable=False,
        null=True,
        blank=True,
        #on_delete=models.CASCADE,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(
        "Date Created", auto_now_add=True,
    )
    odor_identification = models.CharField(
        verbose_name="""
            How many items did you answer correctly (out of 8)
            on the odor identification task?
        """,
        null=True,
        blank=True,
        max_length=4,
    )
    opt_in = models.CharField(
        "I would like to participate in the smell study",
        max_length=4,
        choices=BINARY_CHOICES,
        null=True,
        blank=True,
    )
    mobile = models.BooleanField(
        "I would like to receive health check reminders at my mobile phone.",
        default=False,
    )
    vaccine = models.CharField(
        "I have received a vaccine.",
        max_length=4,
        choices=VACCINE_CHOICES,
        help_text="""
        Valid reasons for not receiving the vaccine are for: religious beliefs;
        health reasons; or personal conviction. If that is the case, you resolve
        to continue wearing masks indoors this fall.
        """,
    )
    vaccine_date = models.DateField(
        help_text="""
        The date of the initial dose for Johnson and Johnson
        or the date of the second dose for Pfizer and Moderna.
        """,
        null=True,
        blank=True,
    )
    vaccine_card_front = models.FileField(
        "Vaccine card front",
        upload_to=upload_to_path,
        help_text="Photo or scan of your COVID-19 vaccine card.",
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS),
        ],
        null=True,
        blank=True,
    )
    vax_rationale = models.TextField(null=True, blank=True)
    uuid = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    contact = models.CharField(max_length=128, null=True, blank=True)
    age = models.CharField(max_length=4, null=True, blank=True)
    biological_sex = models.CharField(max_length=8, null=True, blank=True)
    race = models.ManyToManyField(
        GenericChoice,
        related_name='race',
        help_text = 'Check all that apply',
        null=True,
        blank=True,
    )
    allergy_symptoms = models.CharField(max_length=4, null=True, blank=True)
    smoking_status = models.CharField(max_length=16, null=True, blank=True)
    medications = models.TextField(null=True, blank=True)
    incorrect_items = models.ManyToManyField(
        GenericChoice, null=True, blank=True,
    )

    class Meta:
        """Information about the data class model."""
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self):
        return '{0}, {1}'.format(
            self.user.last_name, self.user.first_name
        )

    def get_perms(self):
        key = 'user_permissions_{0}'.format(self.user.id)
        perms = cache.get(key)
        if not perms:
            perms = {}
            for group in settings.ALL_GROUPS:
                perm = self.user.groups.filter(name=group[0]).exists()
                if perm:
                    perms[group[0]] = group[1]
            cache.set(key, perms)
        return perms

    def get_slug(self):
        return 'registration'

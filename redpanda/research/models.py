# -*- coding: utf-8 -*-

"""Data models."""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from djtools.fields import BINARY_CHOICES
from djtools.fields.helpers import upload_to_path
from redpanda.core.models import GenericChoice
from taggit.managers import TaggableManager


VACCINE_CHOICES = (
    ('Yes', 'I have been vaccinated.'),
    ('No', 'I have a reason not to be vaccinated.'),
)
VACCINE_TYPES = (
    ('Pfizer', 'Pfizer'),
    ('Moderna', 'Moderna'),
    ('Johnson & Johnson', 'Johnson & Johnson'),
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
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
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
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
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
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Date updated", auto_now=True)
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
    vaccine_type = models.CharField(
        max_length=64,
        choices=VACCINE_TYPES,
        null=True,
        blank=True,
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
        validators=settings.FILE_VALIDATORS,
        null=True,
        blank=True,
    )
    booster_date = models.DateField(
        null=True,
        blank=True,
    )
    booster_proof = models.FileField(
        "Proof of booster shot",
        upload_to=upload_to_path,
        help_text="""
          Your COVID-19 vaccine card with the booster date or the receipt from
          the vaccine provider.
        """,
        null=True,
        blank=True,
    )
    vax_rationale = models.TextField(
        "Exemption Rationale",
        null=True,
        blank=True,
    )
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
    incorrect_items = models.ManyToManyField(GenericChoice, null=True, blank=True)

    class Meta:
        """Information about the data class model."""
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self):
        return '{0}, {1}'.format(
            self.user.last_name, self.user.first_name,
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

    def get_group(self):
        perms = self.get_perms()
        groups = []
        for perm, display in perms.items():
            groups.append(display)
        if 'Staff' in groups :
            group = 'Staff'
        elif 'Faculty' in groups:
            group = 'Faculty'
        elif 'Students' in groups:
            group = 'Student'
        else:
            group = 'Staff'
        return group

    def get_slug(self):
        return 'registration'


class Document(models.Model):
    """Supporting documents for a user."""

    #created_at = models.DateTimeField("Date Created", auto_now_add=True)
    created_at = models.DateTimeField()
    #updated_at = models.DateTimeField("Date Updated", auto_now=True)
    updated_at = models.DateTimeField()
    registration = models.ForeignKey(
        Registration,
        related_name='docs',
        on_delete=models.CASCADE,
    )
    phile = models.FileField(
        "Supporting documentation",
        upload_to=upload_to_path,
        validators=settings.FILE_VALIDATORS,
        max_length=767,
        help_text="PDF format",
        null=True,
        blank=True,
    )
    jab_date = models.DateField(
        null=True,
        blank=True,
    )
    tags = TaggableManager(blank=True)

    class Meta:
        ordering  = ['created_at']
        get_latest_by = 'created_at'

    def get_slug(self):
        """Return the slug value for this data model class."""
        return 'registration'

    def get_tags(self):
        """Return tags for this data model class."""
        return [tag for tag in self.tags.all()]


    def __str__(self):
        """Default data for display."""
        return str(self.registration)

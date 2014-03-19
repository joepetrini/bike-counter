from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from model_utils import Choices


class Profile(TimeStampedModel):
    user = models.OneToOneField(User)
    twitter = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = 'profile'


class Organization(TimeStampedModel):
    name = models.CharField(max_length=80)
    city = models.CharField(max_length=25, null=True, blank=True)
    state = models.CharField(max_length=25, null=True, blank=True)
    members = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'organization'


class Membership(TimeStampedModel):
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)

    class Meta:
        db_table = 'membership'
        unique_together = ('user', 'organization')

class Location(TimeStampedModel):
    TYPES = Choices(
        ('intersection', _('Intersection')),
        ('trail', _('Trail')),
        ('bridge', _('Bridge')),
    )
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=80)
    type = models.CharField(choices=TYPES, default=TYPES.intersection, max_length=20)
    longitude = models.CharField(max_length=12, null=True, blank=True)
    latitude = models.CharField(max_length=12, null=True, blank=True)
    has_east = models.BooleanField(default=True)
    has_north = models.BooleanField(default=True)
    has_south = models.BooleanField(default=True)
    has_west = models.BooleanField(default=True)

    class Meta:
        db_table = 'location'


class ValueSet(TimeStampedModel):
    name = models.CharField(max_length=25)
    system_name = models.SlugField(max_length=25, unique=True)

    class Meta:
        db_table = 'valueset'


class Value(TimeStampedModel):
    valueset = models.ForeignKey(ValueSet)
    stored_value = models.CharField(max_length=25)
    display_value = models.CharField(max_length=25)

    class Meta:
        db_table = 'value'


class Metric(TimeStampedModel):
    name = models.CharField(max_length=25)
    desc = models.CharField(max_length=250, null=True, blank=True)
    valueset = models.ForeignKey(ValueSet)

    class Meta:
        db_table = 'metric'


class OrganizationMetrics(TimeStampedModel):
    organization = models.ForeignKey(Organization)
    metric = models.ForeignKey(Metric)

    class Meta:
        db_table = 'org_metrics'
        unique_together = ('organization', 'metric')


class Appointment(TimeStampedModel):
    organization = models.ForeignKey(Organization)
    location = models.ForeignKey(Location)
    user = models.ForeignKey(User, null=True, blank=True)
    scheduled_start = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'appointment'


class Survey(TimeStampedModel):
    appointment = models.ForeignKey(Appointment)
    is_bicycle = models.BooleanField(default=True)
    longitude = models.CharField(max_length=12, null=True, blank=True)
    latitude = models.CharField(max_length=12, null=True, blank=True)

    class Meta:
        db_table = 'survey'


class SurveyValue(TimeStampedModel):
    survey = models.ForeignKey(Survey)
    metric = models.ForeignKey(Metric)
    value = models.ForeignKey(Value)

    class Meta:
        db_table = 'surveyvalue'
        unique_together = ('survey', 'metric')
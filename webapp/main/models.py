#from django.utils.translation import ugettext as _
import datetime
from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from model_utils import Choices


class Organization(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=25, null=True, blank=True)
    state = models.CharField(max_length=25, null=True, blank=True)
    slug = models.SlugField(max_length=15, unique=True)
    member_count = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'organization'

    def __unicode__(self):
        return "%s - %s, %s" % (self.name, self.city, self.state)


class Membership(TimeStampedModel):
    ROLES = Choices(
        ('member', 'member'),
        ('staff', 'staff'),
        ('admin', 'admin'),
    )
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)
    role = models.CharField(choices=ROLES, default=ROLES.member, max_length=15)

    class Meta:
        db_table = 'membership'
        unique_together = ('user', 'organization')

    def __unicode__(self):
        return "%s - %s - %s" % (self.user, self.organization.name, self.role)


class Location(TimeStampedModel):
    TYPES = Choices(
        ('intersection', 'Intersection'),
        ('trail', 'Trail'),
        ('bridge', 'Bridge'),
    )
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=80)
    type = models.CharField(choices=TYPES, default=TYPES.intersection, max_length=20)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    has_east = models.BooleanField(default=True)
    has_north = models.BooleanField(default=True)
    has_south = models.BooleanField(default=True)
    has_west = models.BooleanField(default=True)

    class Meta:
        db_table = 'location'
        ordering = ['name']

    def __unicode__(self):
        return "%s - %s" % (self.organization.name, self.name)


class ValueSet(TimeStampedModel):
    name = models.CharField(max_length=25)
    system_name = models.SlugField(max_length=25, unique=True)

    class Meta:
        db_table = 'value_set'

    def __unicode__(self):
        return self.name


class Value(TimeStampedModel):
    value_set = models.ForeignKey(ValueSet)
    stored_value = models.CharField(max_length=25)
    display_value = models.CharField(max_length=25)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'value'

    def save(self, *args, **kwargs):
        if self.is_default:
            pass
        return super(Value, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s - %s" % (self.valueset, self.display_value)


class Metric(TimeStampedModel):
    name = models.CharField(max_length=25)
    desc = models.CharField(max_length=250, null=True, blank=True)
    value_set = models.ForeignKey(ValueSet)

    class Meta:
        db_table = 'metric'

    def __unicode__(self):
        return "%s - %s - %s" % (self.valueset, self.name, self.desc)


class OrganizationMetrics(TimeStampedModel):
    organization = models.ForeignKey(Organization)
    metric = models.ForeignKey(Metric)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'org_metrics'
        unique_together = ('organization', 'metric')

    def __unicode__(self):
        return "%s - %s" % (self.organization, self.metric)


class Appointment(TimeStampedModel):
    organization = models.ForeignKey(Organization)
    location = models.ForeignKey(Location)
    user = models.ForeignKey(User, null=True, blank=True)
    scheduled_start = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'appointment'

    def __unicode__(self):
        return "%s - %s - %s - %s" % (self.organization.name, self.location, self.user, self.scheduled_start)

    def start(self):
        self.actual_start = datetime.datetime.now()
        self.save()

    def end(self):
        self.actual_end = datetime.datetime.now()
        self.save()

class Survey(TimeStampedModel):
    appointment = models.ForeignKey(Appointment)
    is_bicycle = models.BooleanField(default=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        db_table = 'survey'

    def __unicode__(self):
        return "%s" % (self.appointment)


class SurveyValue(TimeStampedModel):
    survey = models.ForeignKey(Survey)
    metric = models.ForeignKey(Metric)
    value = models.ForeignKey(Value)

    class Meta:
        db_table = 'survey_value'
        unique_together = ('survey', 'metric')

    def __unicode__(self):
        return "%s - %s - %s" % (self.survey, self.metric, self.value)

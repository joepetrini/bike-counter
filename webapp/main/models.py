    #from django.utils.translation import ugettext as _
import datetime
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from django.utils.timezone import now
from model_utils import Choices
from django.utils import timezone

class Organization(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=25, null=True, blank=True)
    state = models.CharField(max_length=25, null=True, blank=True)
    slug = models.SlugField(max_length=15, unique=True)
    member_count = models.IntegerField(null=True, blank=True)
    session_length = models.IntegerField(default=90)

    class Meta:
        db_table = 'organization'

    def __unicode__(self):
        return "%s - %s, %s" % (self.name, self.city, self.state)

    def metrics_list(self):
        return OrganizationMetrics.objects.filter(
            organization=self).values_list('metric__system_name', flat=True)

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
    description = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(choices=TYPES, default=TYPES.intersection, max_length=20)
    enabled = models.BooleanField(default=True)

    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    direction1 = models.CharField(max_length=20, null=True, blank=True)
    direction1_label = models.CharField(max_length=50, null=True, blank=True)
    direction2 = models.CharField(max_length=20, null=True, blank=True)
    direction2_label = models.CharField(max_length=50, null=True, blank=True)

    # Not used
    has_east = models.BooleanField(default=True)
    has_north = models.BooleanField(default=True)
    has_south = models.BooleanField(default=True)
    has_west = models.BooleanField(default=True)


    class Meta:
        db_table = 'location'
        ordering = ['name']

    def __unicode__(self):
        return "%s - %s" % (self.organization.name, self.name)

    def directions(self):
        dirs = []
        if self.has_east:
            dirs.append(Value.objects.get(value_set__system_name='direction', stored_value='east'))
        if self.has_west:
            dirs.append(Value.objects.get(value_set__system_name='direction', stored_value='west'))
        if self.has_north:
            dirs.append(Value.objects.get(value_set__system_name='direction', stored_value='north'))
        if self.has_south:
            dirs.append(Value.objects.get(value_set__system_name='direction', stored_value='south'))
        return dirs



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
        return "%s - %s" % (self.value_set, self.display_value)


class Metric(TimeStampedModel):
    name = models.CharField(max_length=25)
    system_name = models.SlugField(max_length=25, unique=True)
    desc = models.CharField(max_length=250, null=True, blank=True)
    value_set = models.ForeignKey(ValueSet)

    class Meta:
        db_table = 'metric'

    def __unicode__(self):
        return "%s - %s - %s" % (self.name, self.value_set, self.desc)


class Event(TimeStampedModel):
    name = models.CharField(max_length=25)
    system_name = models.SlugField(max_length=25, unique=True)

    class Meta:
        db_table = 'events'

    def __unicode__(self):
        return "%s" % (self.name)


class OrganizationEvents(TimeStampedModel):
    organization = models.ForeignKey(Organization)
    event = models.ForeignKey(Event)

    class Meta:
        db_table = 'org_events'
        unique_together = ('organization', 'event')

    def __unicode__(self):
        return "%s - %s" % (self.organization, self.event)


class OrganizationMetrics(TimeStampedModel):
    organization = models.ForeignKey(Organization)
    metric = models.ForeignKey(Metric)
    required = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    report = models.BooleanField(default=True)

    class Meta:
        db_table = 'org_metrics'
        unique_together = ('organization', 'metric')

    def __unicode__(self):
        return "%s - %s" % (self.organization, self.metric)


class Appointment(TimeStampedModel):
    organization = models.ForeignKey(Organization)
    location = models.ForeignKey(Location)
    user = models.ForeignKey(User, null=True, blank=True, help_text='Leave blank for unassigned')
    scheduled_start = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    time_taken = models.IntegerField(null=True, blank=True)
    longest_pause = models.IntegerField(default=0)
    total_pause = models.IntegerField(default=0)
    total_away = models.IntegerField(default=0)
    # CONSIDER - ADDING NEW FIELD FOR EXPECTED APPT SESSION LENGTH - RIGHT NOW ITS A CONFIG IN BIKE.JS FILE


    class Meta:
        db_table = 'appointment'
        ordering = ['actual_end', 'scheduled_start']

    def __unicode__(self):
        return "%s - %s - %s - %s" % (self.organization.name, self.location, self.user, self.scheduled_start)

    def time_taken_in_min(self):
        return self.time_taken / 60

    def start(self):
        self.actual_start = datetime.datetime.now()
        self.save()

    def end(self, time_taken):
        # per django docs rich changing to using the timezone.now() instead of datetime.datetime.now() as we're using USE_TZ=true
        self.actual_end = timezone.now()
        self.time_taken = int(time_taken)
        self.save()

    def reset(self):
        # Clear data
        for s in self.survey_set.all():
            SurveyValue.objects.filter(survey=s).delete()
        Survey.objects.filter(appointment=self).delete()
        SurveyEvent.objects.filter(appointment=self).delete()
        self.actual_end = None
        self.actual_start = None
        self.time_taken = None
        self.longest_pause = 0
        self.total_pause = 0
        self.total_away = 0
        self.save()

    def complete(self):
        if self.actual_end is None:
            return False
        return True

    def isMorning(self, appt):
        if appt.actual_start.hour < 12:
            return True
        else:
            return False

    def status(self):
        if self.actual_start and self.actual_end is None:
            return "In progress"
        elif self.user is None:
            return "Unassigned"
        elif self.actual_end is None:
            return "Not started"
        return "Complete"






class SessionTrackerViewObject():

    def __init__(self, givenLocation):
        self.thisLocation = givenLocation
        self.amSession1 = None
        self.amSession2 = None
        self.pmSession1 = None
        self.pmSession2 = None

    def assignSessions(self, sessions):

         for cnt in sessions:
          # on 11/22/15 - Rich switched to using the actual start time instead of the scheduled start time
            if cnt.actual_start.time()  < datetime.time(12,00):
                if self.amSession1 is None :
                    self.amSession1 = cnt
                else:
                    self.amSession2 = cnt
            else:
                if self.pmSession1 is None:
                    self.pmSession1 = cnt
                else:
                    self.pmSession2 = cnt
            if self.pmSession2 is not None and self.amSession2 is not None:
                break


class SurveyEvent(TimeStampedModel):
    appointment = models.ForeignKey(Appointment)
    event = models.ForeignKey(Event)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    guid = models.CharField(max_length=50, null=True, blank=True)


    class Meta:
        db_table = 'survey_events'

    def __unicode__(self):
        return "%s - %s - %s" % (self.created, self.appointment, self.event)


class Survey(TimeStampedModel):
    appointment = models.ForeignKey(Appointment)
    is_bicycle = models.BooleanField(default=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time_to_take = models.IntegerField(blank=True, null=True)
    guid = models.CharField(max_length=50, null=True, blank=True)

    # fyi - on 11/24/15 Rich switched to using the datetime.datetime.now() function to resolve timezone discreptency...
    # .. betewen the appointment actual_start and the survey recorded_at variable
    rightnow = datetime.datetime.now()
    recorded_at = models.DateTimeField(default=rightnow)

    direction = models.CharField(max_length=20, null=True, blank=True)

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

#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from main.models import *


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('name', 'type', 'latitude', 'longitude', 'organization',
                  'has_north', 'has_south', 'has_east', 'has_west',
                  'direction1', 'direction2')


class AppointmentSerializer(serializers.ModelSerializer):
    #location = LocationSerializer()

    class Meta:
        model = Appointment
        fields = ('id', 'user')#, 'location', 'scheduled_start', 'actual_start', 'actual_end')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'system_name')


class OrganizationEventSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = OrganizationEvents
        fields = ('organization', 'event')


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ('stored_value', 'display_value', 'is_default', )


class ValueSetSerializer(serializers.ModelSerializer):
    value_set = ValueSerializer()

    class Meta:
        model = ValueSet
        fields = ('system_name', 'value_set')


class MetricSerializer(serializers.ModelSerializer):
    value_set = ValueSetSerializer()

    class Meta:
        model = Metric
        fields = ('name', 'value_set', 'system_name')


class OrganizationMetricSerializer(serializers.ModelSerializer):
    metric = MetricSerializer()

    class Meta:
        model = OrganizationMetrics
        fields = ('organization', 'metric', 'required')


class OrganizationSerializer(serializers.ModelSerializer):
    location_set = LocationSerializer()
    organizationmetrics_set = OrganizationMetricSerializer()
    organizationevents_set = OrganizationEventSerializer()

    class Meta:
        model = Organization
        fields = ('id', 'name', 'city', 'state', 'location_set',
                  'organizationmetrics_set', 'organizationevents_set')


class MembershipSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Membership
        fields = ('organization', 'role')


class UserSerializer(serializers.ModelSerializer):
    appointment_set = AppointmentSerializer()
    #location_set = LocationSerializer()
    #membership_set = MembershipSerializer()
    #membership_set = serializers.RelationsList()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'appointment_set')#, 'membership_set', 'location_set')




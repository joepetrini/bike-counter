#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from main.models import *


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('name', 'type', 'latitude', 'longitude', 'organization')


class AppointmentSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Appointment
        fields = ('id', 'location', 'scheduled_start')


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
        fields = ('organization', 'metric')


class OrganizationSerializer(serializers.ModelSerializer):
    location_set = LocationSerializer()
    organizationmetrics_set = OrganizationMetricSerializer()

    class Meta:
        model = Organization
        fields = ('id', 'name', 'city', 'state', 'location_set', 'organizationmetrics_set')


class MembershipSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Membership
        fields = ('organization', 'role')


class UserSerializer(serializers.ModelSerializer):
    appointment_set = AppointmentSerializer()
    location_set = LocationSerializer()
    membership_set = MembershipSerializer()
    #membership_set = serializers.RelationsList()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'appointment_set', 'membership_set')




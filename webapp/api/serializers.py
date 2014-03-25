from django.contrib.auth.models import User, Group
from rest_framework import serializers
from main.models import Membership, Location, Appointment, Organization


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('name', 'type', 'latitude', 'longitude')


class AppointmentSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Appointment
        fields = ('location', 'scheduled_start')


class OrganizationSerializer(serializers.ModelSerializer):
    location_set = LocationSerializer()

    class Meta:
        model = Organization
        fields = ('name', 'city', 'state', 'location_set')


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




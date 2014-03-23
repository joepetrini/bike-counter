from django.contrib.auth.models import User, Group
from rest_framework import serializers
from main.models import Organization, Location


class UserSerializer(serializers.ModelSerializer):
    appointment_set = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'appointment_set')


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('name', 'type', 'lat', 'long')


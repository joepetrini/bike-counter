from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, LocationSerializer, AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import authentication
from main.models import Organization, Location, Appointment, Survey, SurveyValue, Metric, Value


class LocationViewSet(viewsets.ModelViewSet):
    """
    Get all locations for an org
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class MeDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    #def get_object(self, pk):
    #    return self.request.user

    def get(self, request, format=None):
        if request.user.is_authenticated():
            print type(request.user)
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)


class ApptViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    @action(methods=['POST'])
    def start(self, request, pk=None):
        appt = self.get_object()
        # TODO: check that appointment is not complete
        appt.start()
        return Response(None, status=status.HTTP_200_OK)

    @action(methods=['POST'])
    def end(self, request, pk=None):
        appt = self.get_object()
        appt.end()
        return Response(None, status=status.HTTP_200_OK)

    @action(methods=['POST'])
    def survey(self, request, pk=None):
        appt = self.get_object()
        # TODO: check that appointment is not complete
        # Create a new survey
        survey = Survey(appointment=appt)
        print survey
        survey.save()
        for k, v in request.DATA.items():
            try:
                metric = Metric.objects.get(system_name=k)
                value = Value.objects.get(value_set=metric.value_set, stored_value=v)
                sv, c = SurveyValue.objects.get_or_create(survey=survey, metric=metric, value=value)
            except Metric.DoesNotExist:
                continue
            except Value.DoesNotExist:
                print "Value does not exist %s in %s" % (k, v)
            print "%s %s" % (k, v)
        return Response(None, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


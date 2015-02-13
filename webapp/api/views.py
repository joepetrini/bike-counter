from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, LocationSerializer, AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route #action
#from rest_framework import authentication
from main.models import Organization, Location, Appointment, Survey, SurveyValue, Metric, Value, Event, SurveyEvent


class LocationViewSet(viewsets.ModelViewSet):
    """
    Get all locations for an org
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


#class OrgViewSet(viewsets.ModelViewSet):
#    queryset = Membership.objects.all()
#    serializer_class = OrganizationSerializer


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

    #@action(methods=['POST'])
    @detail_route(methods=['POST'])
    def start(self, request, pk=None):
        appt = self.get_object()
        # TODO: check that appointment is not complete
        appt.start()
        return Response(None, status=status.HTTP_200_OK)

    #@action(methods=['POST'])
    @detail_route(methods=['POST'])
    def end(self, request, pk=None):
        appt = self.get_object()
        appt.end(request.DATA['total_time'])
        appt.total_pause = int(request.DATA['total_pause'])
        appt.longest_pause = int(request.DATA['longest_pause'])
        appt.total_away = int(request.DATA['total_away'])
        appt.save()
        return Response(None, status=status.HTTP_200_OK)

    #@action(methods=['POST'])
    @detail_route(methods=['POST'])
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

    #@action(methods=['POST'])
    @detail_route(methods=['POST'])
    def event(self, request, pk=None):
        appt = self.get_object()
        for k, v in request.DATA.items():
            print "{} {}".format(k, v)
        # TODO get event type and add to related survey
        ev = Event.objects.get(id=request.DATA['event_id'])
        se = SurveyEvent.objects.create(appointment=appt, event=ev)
        return Response(None, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


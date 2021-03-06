from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, LocationSerializer, AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route  # action
# from rest_framework import authentication
from main.models import Organization, OrganizationMetrics, Location, Appointment, Survey, SurveyValue, Metric, Value, \
    Event, SurveyEvent
import datetime
from main.logic import *
import json
from django.http import JsonResponse
from main.views import RequestCSVView

class CurrentUser(APIView):
    def get(self, request):
            serializer = UserSerializer(request.user)
            return Response(serializer.data)


def grabAppts(request, slug):
    response_data = {}
    #try:
    response_data['result'] = "Success"

    response_data['appointment_choices'] = list(get_appts_choices(request.current_org, request.POST.get('year_selection',None)))

    return JsonResponse(response_data, status=status.HTTP_200_OK)

class LocationViewSet(viewsets.ModelViewSet):
    """
    Get all locations for an org
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


#class OrgViewSet(viewsets.ModelViewSet):
#    queryset = Membership.objects.all()
#    serializer_class = OrganizationSerializer


class ApptDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    #def get_object(self, pk):
    #    return self.request.user

    def get(self, request, format=None):
        if request.user.is_authenticated():
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

class singleCompletedAppt(viewsets.ModelViewSet):
    # Trying to create a new view to support showing a single appointment's stats highlights on the mobile app's "completed survey" view
    # this is associated to the #appstates template fragment in the index.html file


    queryset = Appointment.objects.all()
    #serializer_class = Stats_for_appt_Serializer
    serializer_class = AppointmentSerializer

    @detail_route(methods=['GET'])
    def get(self, request, pk=None):
        if request.user.is_authenticated():
            appt = self.get_object()
            theStats = stats_for_appt(appt)
            #serializer = Stats_for_appt_Serializer(theStats)

            return Response(theStats, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)



class ApptViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


    @detail_route(methods=['POST'])
    def start(self, request, pk=None):
        appt = self.get_object()
        # TODO: check that appointment is not complete
        appt.start()
        return Response(None, status=status.HTTP_200_OK)


    @detail_route(methods=['POST'])
    def end(self, request, pk=None):
        appt = self.get_object()
        appt.end(request.DATA['total_time'])
        appt.total_pause = int(request.DATA['total_pause'])
        appt.longest_pause = int(request.DATA['longest_pause'])
        appt.total_away = int(request.DATA['total_away'])
        appt.save()
        return Response(None, status=status.HTTP_200_OK)


    @detail_route(methods=['GET'])
    def reset(self, request, pk=None):
        appt = self.get_object()
        if request.user.is_superuser or request.user == appt.user:
            appt.reset()
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)


    @detail_route(methods=['POST'])
    def survey(self, request, pk=None):
        appt = self.get_object()
        # TODO: check that appointment is not complete

        # Create a new survey
        direction = str(request.DATA['direction']).lower()
        guid = str(request.DATA['guid']).lower()

        # needed to add the recorded_at variable into this as this survey could post "late" due to poor connectivity
        recorded_at_timestamp = float(request.DATA['timestamp'])
        recorded_at_timestamp = datetime.datetime.fromtimestamp(recorded_at_timestamp/1000.0)

        survey = Survey.objects.create(appointment=appt, direction=direction, guid=guid, recorded_at=recorded_at_timestamp)

        # Get the available metric system_names for this org
        metrics = appt.organization.metrics_list()
        for k, v in request.DATA.items():
            try:
                # If posted data is in expected metrics, save it
                if str(k).lower() in metrics:
                    metric = Metric.objects.get(system_name=k)
                    value = Value.objects.get(value_set=metric.value_set, stored_value=v)
                    sv, c = SurveyValue.objects.get_or_create(survey=survey, metric=metric, value=value)
                    print "Saving %s = %s" % (k, v)
            except Metric.DoesNotExist:
                print "Metric does not exist metric:sys_name=%s    value:stored_val=%s" % (k, v)
            except Value.DoesNotExist:
                print "Value does not exist metric:sys_name=%s     value:stored_val=%s" % (k, v)

        return Response(None, status=status.HTTP_200_OK)


    @detail_route(methods=['POST'])
    def event(self, request, pk=None):
        appt = self.get_object()
        for k, v in request.DATA.items():
            print "{} {}".format(k, v)
        ev = Event.objects.get(id=request.DATA['event_id'])
        guid = request.DATA['guid']
        se = SurveyEvent.objects.create(appointment=appt, event=ev, guid=guid)
        return Response(None, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """s
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer




#from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
#from django.views.generic.edit import FormView
from .models import Organization, Appointment, Membership, Location, SessionTrackerViewObject
from .logic import stats_for_appt, csv_for_appt
import datetime
import time
import csv
from django.shortcuts import get_object_or_404

class OrgListView(ListView):
    model = Organization
    template_name = 'select_org.html'

    def render_to_response(self, context, **response_kwargs):
        # If there's only 1 org in the system, auto assign and move on
        if Organization.objects.all().count() > 0:  # == 1:
            org = Organization.objects.all()[0]
            mem = Membership.objects.get_or_create(user=self.request.user, organization=org)
            return HttpResponseRedirect(reverse('org_home', args=[org.slug]))
        else:
            pass

    #def get_queryset(self):
    #    pass


class OrgHomeView(DetailView):
    model = Organization
    template_name = 'org_home.html'

    def get_context_data(self, **kwargs):
        context = super(OrgHomeView, self).get_context_data(**kwargs)
        sessions = Appointment.objects.filter(user=self.request.user, organization=self.object)
        unassigned = Appointment.objects.filter(user=None, organization=self.object)
        context['sessions'] = sessions
        context['unassigned'] = unassigned
        if self.request.user.is_superuser:
            all = Appointment.objects.filter(organization=self.object)
            context['all'] = all
        return context


class ApptDetailView(DetailView):
    model = Appointment
    template_name = 'appointment_detail.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.has_key('csv'):
            out = csv_for_appt(self.object)
            return HttpResponse(content=out)#, content_type='text/csv')
        else:
            return super(ApptDetailView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(ApptDetailView, self).get_context_data(**kwargs)
        context['stats'] = stats_for_appt(self.object)
        return context


class ApptCancelView(DetailView):
    model = Appointment

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == request.user:
            obj.user = None
            obj.save()
        return HttpResponseRedirect(reverse('org_home', args=[obj.organization.slug]))


class ApptSignupView(DetailView):
    model = Appointment

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect(reverse('org_home', args=[obj.organization.slug]))

class OrgScheduleView(ListView):
    model = Location
    template_name = 'org_schedule.html'

    #def render_to_response(self, context, **response_kwargs):
    #    pass

    #def get_queryset(self):
    #    pass


class ReportHomeView(ListView):
    model = Appointment
    template_name = 'report_home.html'


class ReportCompletionTrackerView(TemplateView):
    template_name = 'report_count_completion_tracker.html'



    def get_context_data(self, **kwargs):
        context = super(ReportCompletionTrackerView, self).get_context_data(**kwargs)

        theTrackerSessions=[]
        theOrg = Organization.objects.get(slug=self.request.current_org)
        allLocations = Location.objects.filter(organization=theOrg)

        for counter in allLocations:
           # cntLoc = sessions[counter].location scheduled_start__year='2015'

           #instantiate a new object
           singleLocationSet = SessionTrackerViewObject(counter)

           # query the db for all appointments for the given location, in the given year, given org
           #sessions =[]
           sessions = Appointment.objects.filter(organization=Organization.objects.get(slug=self.request.current_org), location=counter, scheduled_start__year =  datetime.date.today().year)

          # call method of SessionTrackerViewObject that will determine with appointments should be considered the 4 key appointments
           singleLocationSet.assignSessions(sessions)

           # push the new object onto the list which will be used by the html template
           theTrackerSessions.append(singleLocationSet)

        context['trackerSessions'] = theTrackerSessions

        #context['trackerSessions'] = sessions
        context['org'] = theOrg
        return context



class ReportLocationsView(TemplateView):
    template_name = 'report_locations.html'

    def get_context_data(self, **kwargs):
        context = super(ReportLocationsView, self).get_context_data(**kwargs)
        context['org'] = Organization.objects.get(slug=self.request.current_org)
        return context

class RequestCSVView(TemplateView):

    #Rich's ideas on how to: psuedo steps
    # 1 - Provide user controls on web page to identify what selection of data they would like to export - for starters, we can only offer a "full year's worth"
    # 1.5 - user hits "go" button that requests the CSV be generated
    # check back every few half seconds (??) to see if file generated has been completed
    #2 - then use that user selection to query/ filter our django / postgresql tables to retrieve the data
    # 3 - finally - use baked in django (or is it python) functionts to export data into a csv file format --- but remember to build the file in the output required

    template_name = 'report_export_to_csv.html'
    def get_context_data(self, **kwargs):
        context = super(RequestCSVView, self).get_context_data(**kwargs)

        context['org'] = Organization.objects.get(slug=self.request.current_org)
        return context

class GenerateCSV(RequestCSVView):


    model = Organization

    def get(self, request, *args, **kwargs):

        #call separate function to create the actual file
        #fileToBeProvided = createCSVExportFile(2015)

        theFileContent = ('Intersection or Bridge,Street,Facility for Street,Direction,Date,15 minute increment,TOTAL Riders (not counting bike on buses),'
            'With traffic male,With traffic female,sidewalk male,Sidewalk female,wrong way male,wrong way female,bikes on bus,Completed By,Latitute,'
            'Longitude,Helmet male,Helmet female,Weather,temperature,Notes')

        theFilename = 'export_' + (datetime.date.today().strftime("%I%M")) + '_data_for_filemaker.csv'
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=%s;' % str(theFilename)

        writer = csv.writer(response)
        writer.writerow([theFileContent])


        return response

class ReportQuickGlanceResultsDashboardView(TemplateView):
    template_name = 'results_dashboard.html'
    def get_context_data(self, **kwargs):
        context = super(ReportQuickGlanceResultsDashboardView, self).get_context_data(**kwargs)
      #  context['org'] = Organization.objects.get(slug=self.request.current_org)
        return context
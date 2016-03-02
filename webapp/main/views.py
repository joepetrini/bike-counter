#from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, FormView
#from django.views.generic.edit import FormView
from .models import Organization, Appointment, Membership, Location, SessionTrackerViewObject, Survey, SurveyValue, SurveyEvent
from .logic import *
import datetime
import time
import csv

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import detail_route
from datetime import timedelta
from .forms import CSV_report_selection_form

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
           # TODO - current feature gap is that this filter and page only shows the current years appointment tracking. really we should lett the user select the year
           sessions = Appointment.objects.filter(organization=Organization.objects.get(slug=self.request.current_org), location=counter, actual_start__year =  datetime.date.today().year)

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




class RequestCSVView(FormView):

    #Rich's ideas on how to: psuedo steps
    # 1 - Provide user controls on web page to identify what selection of data they would like to export - for starters, we can only offer a "full year's worth"
    # 1.5 - user hits "go" button that requests the CSV be generated
    # check back every few half seconds (??) to see if file generated has been completed
    #2 - then use that user selection to query/ filter our django / postgresql tables to retrieve the data
    # 3 - finally - use baked in django (or is it python) functionts to export data into a csv file format --- but remember to build the file in the output required
    template_name = 'report_export_to_csv.html'

    form_class = CSV_report_selection_form

    def get_success_url(self, org):
        success_url = reverse_lazy('generateCSV', kwargs={'slug': org})
        return success_url


    def get_year_choices(self):
        #get all available appointments for the given year the user selects
        unique_years_choices = []

        allyearsQuery = Appointment.objects.filter(organization = Organization.objects.get(slug=self.request.current_org)).datetimes('scheduled_start','year')

        for a in allyearsQuery:
            unique_years_choices += [(a.year, a.year )]

        return unique_years_choices





    def get(self, request, *args, **kwargs):

        currentYear = datetime.datetime.now().year
        theOrg = self.request.current_org
        # I want to update this to make a bound form (after reading)
        all_appts = get_appts_choices(theOrg, currentYear)
        unique_years = self.get_year_choices()

        form = CSV_report_selection_form(
           yrinit = str(currentYear),
           yr_choices = unique_years,
           appt_choices = all_appts
        )

        return render(request, 'report_export_to_csv.html', {'form': form.as_p, 'org':theOrg } )


    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        errors = []

        theOrg = self.request.current_org

        unique_years = self.get_year_choices()

        formData = {}
        formData['year_selection'] = request.POST.get('year_selection',None)
        formData['appt_selection'] = request.POST.get('appt_selection',None)


        #creating my own basic "validate data" logic
        if (i for i, v in enumerate(unique_years) if v[0] == formData['year_selection']):
                pass
        else:
            errors.append("select a valid year")


        if(i for i, v in enumerate(get_appts_choices(theOrg,  formData['year_selection'])) if v[0] == formData['appt_selection']):
            pass
        else:
            errors.append("you must select a valid appointment")


        currentYear = datetime.datetime.now().year
        all_appts = get_appts_choices(theOrg, currentYear)
        form = CSV_report_selection_form(
           yrinit = str(currentYear),
           yr_choices = unique_years,
           appt_choices = all_appts
        )



        if len(errors) == 0:
            return self.createCSVReport(self.request, formYear=formData['year_selection'] , formAppt=formData['appt_selection']  )
        else:

            return (request, 'report_export_to_csv.html', {'form': form.as_p, 'org':self.request.current_org, 'errors': errors } )

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.



    def createCSVReport(self, request, *args, **kwargs):

        #this will be from the user's selection on the web form - if none given use the current year
        formYearSelection = kwargs.get('formYear', datetime.datetime.now().year)
        # this will be from the user's selection on the web form - defaults to ALL
        formApptSelection = kwargs.get('formAppt', "ALL")


        theFileContent = ['Appointment ID', 'Intersection or Bridge', 'Street', 'Facility for Street']
        theFileContent += ['Direction', 'Actual Survey Date', '15 minute increment', 'TOTAL Riders (not counting bike on buses)']
        theFileContent += ['With traffic male', 'With traffic female', 'sidewalk male', 'Sidewalk female']
        theFileContent += ['wrong way male', 'Wrong way female', 'bikes on bus', 'Completed By' ,'Latitute']
        theFileContent += ['Longitude', 'Helmet male', 'Helmet female', 'Count Year', 'Weather', 'temperature', 'Notes']

        #theFilename = 'export_' + (datetime.datetime.now().strftime("%I%M")) + '_data_for_filemaker.csv'
        theFilename = 'filemakerExport_of_' + str(formYearSelection) + "_" + str(formApptSelection) + '_pulledOn_' + (datetime.datetime.now().strftime("%I%M")) + '.csv'
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=%s;' % str(theFilename)

        writer = csv.writer(response)
        writer.writerow(theFileContent)

        #below IF statement uses form selection to pull the right appointments for the CSV
        #If ALL that meant the user wanted all the appts for a given year
        #if any other value for the appt selection, we should pull all the appts for the given year


        if formApptSelection == 'ALL':
            appts_in_scope = Appointment.objects.filter(scheduled_start__year = formYearSelection, organization=Organization.objects.get(slug=self.request.current_org))
        else:
            appts_in_scope = Appointment.objects.filter(id=int(formApptSelection), organization=Organization.objects.get(slug=self.request.current_org))



        for x in appts_in_scope:
            allSurveysForApptInScope = Survey.objects.filter(appointment_id = x.id)


            #inserting Try/catch so avoid errors where appointments don't have an actual start dates yet
            try:
                apptStartTime = x.actual_start


                currentInterval = apptStartTime
                endTime = apptStartTime + timedelta(minutes=90)


                #using a massive for loop to cycle through all 15 minute intervals found within the survey
                #some day this could be put into its on method or class
                # ASSUMPTION - I'll start the looping of 15 minute increments at the ACTUAL start time
                # actual_start through 90 minutes from actual start jumping in 15 minute increments


                while currentInterval < endTime:
                    # next item needs to be the cardinal direction being summarized --- aka n/s/e/w
                    # WIP - so to do this, I should loop through 2 different directions - direction1 and direction 2 that each appoitnments' location has
                    # so for loop through all an appointment's survey's where the survey-item's direction is = direction 1

                    allDirs = ['direction1', 'direction2']
                    for i in allDirs:

                        csvOutputString = []
                        #appointment ID
                        csvOutputString += [x.id]
                        csvOutputString = [x.location.name]
                        if i == 'direction1':
                            #query for direction 1 data
                            # WILL NEED TO LIKELY PRE-QUERY DIRECTION 1 DATA HERE
                            currentDirection = x.location.direction1
                            currentCardinalDirectionSummary = 'North/South'

                            #Note, this will actually be labeled as street on the final csv output.
                            csvOutputString += [x.location.direction1]

                            # As of 11/1/15 - I don't believe we have a dedicated attribution of a location to represent "cardinal direction"
                            # Also remember that currently the bike coalition only summarized cardinal directions 2-ways ..... N/S and E/W
                            # instead - proposed logic - IF bridge or trail type, then obviously the only direction is east/west
                            # else - assuming an Intersection type, perhaps start with N/S, then go to E/W .....
                            # this assumes there will always be intersections with both sets -which as of now, there is -worst case, we report 'zeros'


                        else:
                            #query for direction 2 data

                            currentDirection = x.location.direction2
                            currentCardinalDirectionSummary = 'East/West'
                             #Note, this will actually be labeled as street on the final csv output.
                            csvOutputString += [x.location.direction2]

                        endofCurrentInterval = currentInterval + timedelta(minutes=15)
                        currentDirection = currentDirection.lower()
                        currentSubSurveysByDirectionAndInterval = allSurveysForApptInScope.filter(direction=currentDirection, recorded_at__range=(currentInterval,endofCurrentInterval))


                        csvOutputString += ['STREET FACILITY that we dont have']
                        csvOutputString += [currentCardinalDirectionSummary]

                        # then is the date of the survey
                        csvOutputString += [x.actual_start.strftime("%m/%d/%Y")]

                        #then the 15 minute interval being summarized -- ex of formatting 7:30-7:45 AM
                        csvOutputString += [currentInterval.strftime("%I:%M") + '-' + endofCurrentInterval.strftime("%I:%M %p")]

                        # then total riders --- all survey entries for a given appointment in a given 15 minute range, in a given direction
                        csvOutputString += [currentSubSurveysByDirectionAndInterval.count()]

                        # With traffic male - REQUIRES join with survey-values table

                        surveyValues_subset_all = SurveyValue.objects.filter(survey__in=list(currentSubSurveysByDirectionAndInterval))

                        #start by pre-pulling all SV's that are for males
                        maleSurveyValues = surveyValues_subset_all.filter(metric__system_name = 'gender', value__stored_value='m').values('survey')

                        #then pre-pull all SV's for sidewalk riders
                        sidewalkSurveyValues =surveyValues_subset_all.filter(metric__system_name = 'sidewalk', value__stored_value = 'yes').values('survey')

                        #then pre-pull all SV's for wrong way riders
                        wrongwaySurveyValues =surveyValues_subset_all.filter(metric__system_name = 'wrong_way', value__stored_value = 'yes').values('survey')

                        #to get with traffic male tally I 1st filter for only male riders
                        withTrafficMaleTally = currentSubSurveysByDirectionAndInterval.filter(id__in = (maleSurveyValues))
                        #Then from that subset, I then want to exclude any survey IDs that are in a list of sidewalk riders
                        withTrafficMaleTally = withTrafficMaleTally.exclude(id__in = (sidewalkSurveyValues))
                        #then, I further want to exclude wrong way riders - just in case really
                        withTrafficMaleTally = withTrafficMaleTally.exclude(id__in = (wrongwaySurveyValues))

                        withTrafficMaleTally = withTrafficMaleTally.count()
                        csvOutputString += [withTrafficMaleTally]

                        #with traffic female
                        #start by pre-pulling all SV's that are for FEMALES
                        femaleSurveyValues = surveyValues_subset_all.filter(metric__system_name = 'gender', value__stored_value='f').values('survey')

                        #then pre-pull all SV's for sidewalk riders
                        sidewalkSurveyValues =surveyValues_subset_all.filter(metric__system_name = 'sidewalk', value__stored_value = 'yes').values('survey')

                        #then pre-pull all SV's for wrong way riders
                        wrongwaySurveyValues =surveyValues_subset_all.filter(metric__system_name = 'wrong_way', value__stored_value = 'yes').values('survey')

                        #to get with traffic male tally I 1st filter for only FEMALE riders
                        withTrafficFemaleTally = currentSubSurveysByDirectionAndInterval.filter(id__in = (femaleSurveyValues))
                        #Then from that subset, I then want to exclude any survey IDs that are in a list of sidewalk riders
                        withTrafficFemaleTally = withTrafficFemaleTally.exclude(id__in = (sidewalkSurveyValues))
                        #then, I further want to exclude wrong way riders - just in case really
                        withTrafficFemaleTally = withTrafficFemaleTally.exclude(id__in = (wrongwaySurveyValues))

                        withTrafficFemaleTally = withTrafficFemaleTally.count()

                        csvOutputString += [withTrafficFemaleTally]

                        # sidewalk male ---
                        # NOTE - AS OF 12/16 still working on this

                        sidewalkMaleTally = currentSubSurveysByDirectionAndInterval.filter(id__in = (maleSurveyValues))
                        sidewalkMaleTally = sidewalkMaleTally.exclude(id__in = (wrongwaySurveyValues))
                        sidewalkMaleTally = sidewalkMaleTally.filter(id__in = sidewalkSurveyValues)

                        csvOutputString += [sidewalkMaleTally.count()]

                        #then 	sidewalk female
                        sidewalkFemaleTally = currentSubSurveysByDirectionAndInterval.filter(id__in = (femaleSurveyValues))
                        sidewalkFemaleTally = sidewalkFemaleTally.exclude(id__in = (wrongwaySurveyValues))
                        sidewalkFemaleTally = sidewalkFemaleTally.filter(id__in = sidewalkSurveyValues)

                        csvOutputString += [sidewalkFemaleTally.count()]

                        #then wrong way male
                        wrongWayMaleTally = currentSubSurveysByDirectionAndInterval.filter(id__in = (maleSurveyValues))
                        wrongWayMaleTally = wrongWayMaleTally.filter(id__in = (wrongwaySurveyValues))
                        wrongWayMaleTally = wrongWayMaleTally.exclude(id__in = sidewalkSurveyValues)

                        csvOutputString += [wrongWayMaleTally.count()]

                        #wrong way female
                        wrongWayFemaleTally = currentSubSurveysByDirectionAndInterval.filter(id__in = (femaleSurveyValues))
                        wrongWayFemaleTally = wrongWayFemaleTally.filter(id__in = (wrongwaySurveyValues))
                        wrongWayFemaleTally = wrongWayFemaleTally.exclude(id__in = sidewalkSurveyValues)

                        csvOutputString += [wrongWayFemaleTally.count()]

                        #bikes on bus
                        surveyEventsForGivenPeriod = SurveyEvent.objects.filter(appointment_id = x.id, created__range=(currentInterval,endofCurrentInterval))
                        bikesOnBustally = surveyEventsForGivenPeriod.filter(event__pk=1).count()
                        csvOutputString += [bikesOnBustally]

                        #Completed By
                        apptVolunteer = x.user.get_full_name()
                        csvOutputString += [apptVolunteer]

                        #Latitude
                        latitudeValue = x.location.latitude
                        csvOutputString += [latitudeValue]

                        #Longitude
                        longitudeValue = x.location.longitude
                        csvOutputString += [longitudeValue]

                        #helmet male - first I need to pull all the survey-value entries for helmets
                        allHelmetSurveyValues = surveyValues_subset_all.filter(metric__system_name = 'helmet', value__stored_value = 'yes').values('survey')

                        helmetMaleTally = currentSubSurveysByDirectionAndInterval.filter(id__in = (maleSurveyValues))
                        helmetMaleTally = helmetMaleTally.filter(id__in = (allHelmetSurveyValues))

                        csvOutputString += [helmetMaleTally.count()]

                        #helmet female
                        helmetFemaleTally = currentSubSurveysByDirectionAndInterval.filter(id__in = (femaleSurveyValues))
                        helmetFemaleTally = helmetFemaleTally.filter(id__in = (allHelmetSurveyValues))

                        csvOutputString += [helmetFemaleTally.count()]


                        #appointment count year
                        csvOutputString += [x.scheduled_start.strftime("%Y")]

                        #weather
                        csvOutputString +=['THIS COUNT BE A WEATHER FIELD']

                        #temperature
                        csvOutputString += ['THIS COULD BE TEMPERATURE']

                        #notes
                        csvOutputString += ['THIS COULD BE A NOTES FIELD']




                        #BOTTOM OF FOR LOOP
                        writer.writerow(csvOutputString)

                    currentInterval += timedelta(minutes=15)
                    # BOTTOM OF WHILE LOOP

            except TypeError:
                print "error because no actual start and no actual data"

                csvOutputString = [x.id, x.location.name]
                csvOutputString += ['NO DATA FOR THIS APPOINTMENT']
                writer.writerow(csvOutputString)

        return response





class ReportQuickGlanceResultsDashboardView(TemplateView):
    template_name = 'results_dashboard.html'
    def get_context_data(self, **kwargs):
        context = super(ReportQuickGlanceResultsDashboardView, self).get_context_data(**kwargs)
      #  context['org'] = Organization.objects.get(slug=self.request.current_org)
        return context
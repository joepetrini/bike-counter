import random
from datetime import datetime
from django.db import transaction
from django.utils.timezone import now
from .models import *


def csv_for_appt(appt):
    out = ''
    # Headers
    out += "Time,Bike,Direction,"
    for m in appt.organization.organizationmetrics_set.all():
        out += "%s," % m.metric.name
    out = out[:-1] + "\n"

    # Detail
    for s in appt.survey_set.all():
        out += "%s,%s,%s," % (s.created, s.is_bicycle, s.direction)
        for sv in s.surveyvalue_set.all():
            out += "%s," % sv.value.stored_value
        out = out[:-1] + "\n"
    return out



def stats_for_appt(appt):
    stat = {}
    stat['total'] = appt.survey_set.all().count()
    metrics = {}

    min = {}
    for i in range(0, ((appt.actual_end - appt.actual_start).seconds / 60)):
        min[i] = 0

    metrics[-1] = {'name': 'direction', 'stats': {}}

    # List of metrics
    for m in appt.organization.organizationmetrics_set.filter(report=True):
        metrics[m.metric.id] = {'name': m.metric.name, 'stats': {}}

    # Value counts across all recorded info
    for s in appt.survey_set.all():
        # Direction
        try:
            metrics[-1]['stats'][s.direction] += 1
        except KeyError:
            metrics[-1]['stats'][s.direction] = 1


        minutes_in = (s.recorded_at - appt.actual_start).seconds / 60
        try:
            min[minutes_in] += 1
        except KeyError:
            min[minutes_in] = 1

        for sv in s.surveyvalue_set.select_related().all():
            # Not in reportable metrics
            if sv.metric.id not in metrics.keys():
                continue

            try:
                metrics[sv.metric.id]['stats'][sv.value.display_value] += 1
            except KeyError:
                metrics[sv.metric.id]['stats'][sv.value.display_value] = 1
    print min
    stat['metrics'] = metrics
    stat['minutes'] = min
    return stat



def sim_appt(appt, avg_time=25):
    with transaction.atomic():
        # Clear data
        appt.reset()
        #for s in appt.survey_set.all():
        #    SurveyValue.objects.filter(survey=s).delete()
        #Survey.objects.filter(appointment=appt).delete()

        start = now()
        total_time = 0

        while True:
            sec = random.randint(0, avg_time * 2)
            total_time += sec

            t = start + datetime.timedelta(seconds=total_time)
            s = Survey.objects.create(appointment=appt, recorded_at=t)

            for m in appt.organization.organizationmetrics_set.all():
                metric = m.metric
                if metric.value_set.system_name == 'direction':
                    val = random.choice(list(appt.location.directions()))
                else:
                    val = random.choice(list(m.metric.value_set.value_set.all()))
                # TODO handle defaults
                has_def = m.metric.value_set.value_set.filter(is_default=True).count()
                sv = SurveyValue.objects.create(survey=s, metric=metric, value=val)

            # TODO Add events

            if total_time > appt.organization.session_length * 60:
                break

        appt.actual_start = start
        appt.actual_end = start + datetime.timedelta(0, total_time)
        appt.time_taken = total_time
        appt.save()

def get_appts_choices(theOrg, theYear=None):

    all_appts_choices = [('default', '--Pick--'),('ALL', 'Download All Appointments')]
    if theYear is not None:
        all_appts_choices += [(a['id'],
        (str(a['id']) + ' - ' + str(a['location__name'])) )
        for a in Appointment.objects.filter(scheduled_start__year = theYear, organization = Organization.objects.get(slug=theOrg)).order_by('id').values('id', 'location__name') ]

    else:
        all_appts_choices += [(a['id'],
        (str(a['id']) + ' - ' + str(a['location__name'])) )
        for a in Appointment.objects.filter(organization = Organization.objects.get(slug=theOrg)).order_by('id').values('id', 'location__name') ]


        #for the count year drown-down, pull down all unique start_date years for the appts in the dB
        # to accomodate for potential DB compatibilities with django's distinct() function (only postgreSQL works), I'll do the unique year filtering myself

    return all_appts_choices

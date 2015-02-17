import random
from datetime import datetime
from django.db import transaction
from django.utils.timezone import now
from .models import *


def csv_for_appt(appt):
    out = ''
    # Headers
    out += "Time,Bike,"
    for m in appt.organization.organizationmetrics_set.all():
        out += "%s," % m.metric.name
    out = out[:-1] + "\n"
    for s in appt.survey_set.all():
        out += "%s,%s," % (s.created, s.is_bicycle)
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

    # List of metrics
    for m in appt.organization.organizationmetrics_set.filter(report=True):
        metrics[m.metric.id] = {'name': m.metric.name, 'stats': {}}

    # Value counts across all recorded info
    for s in appt.survey_set.all():
        i = (s.recorded_at - appt.actual_start).seconds / 60
        try:
            min[i] += 1
        except KeyError:
            min[i] = 1

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
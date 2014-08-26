from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from main.models import Location, Organization, Appointment


class Command(BaseCommand):
    help = 'Created unassigned appts for locations'

    def handle(self, *args, **options):
        org = Organization.objects.all()[0]
        locations = Location.objects.filter(organization=org, enabled=True)

        from_date = datetime.today() - timedelta(days=30)
        sched_date = datetime.today() + timedelta(days=10)

        for loc in locations:
            # Check that location has 2 appts from last 30 days forward
            appt_count = Appointment.objects.filter(organization=org, location=loc, scheduled_start__gt=from_date).count()
            if appt_count < 2:
                print "missing appts for %s - %s found" % (loc, appt_count)
                for i in range(0, 2 - appt_count):
                    print("Creating appt for %s" % (loc))
                    Appointment.objects.create(organization=org, location=loc, scheduled_start=sched_date)
from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main.logic import sim_appt


class Command(BaseCommand):
    args = 'Usage: sim_app <appt_id>'
    help = 'Auto fills data for an appt'

    def handle(self, *args, **options):
        if len(args) != 1:
            print self.args
            return

        # Get the appt
        appt = Appointment.objects.get(id=int(args[0]))

        sim_appt(appt)

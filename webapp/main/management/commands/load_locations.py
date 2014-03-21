from django.core.management.base import BaseCommand, CommandError
import gspread
from main.models import Location, Organization


class Command(BaseCommand):
    args = 'Usage: load_locations <google_user> <google_pass>'
    help = 'Load locations from google spreadsheet'

    def handle(self, *args, **options):
        if len(args) != 2:
            print self.args
            return
        org = Organization.objects.all()[0]
        key = '0AgUErk7rE6TLdGJ0NE90U2pDVE9MRkZrU2hGR0FhRlE'
        gc = gspread.login(args[0], args[1])
        sht = gc.open_by_key(key).get_worksheet(0)
        values = sht.get_all_values()
        for v in values[1:]:
            [name, type, lat, long] = v
            loc, c = Location.objects.get_or_create(organization=org, name=name)
            loc.type = type
            loc.lat = lat
            loc.long = long
            loc.save()
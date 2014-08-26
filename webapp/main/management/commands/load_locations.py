from django.core.management.base import BaseCommand, CommandError
import gspread
from main.models import Location, Organization


def to_bool(v):
    if str(v).lower() == 'y':
        return True
    return False


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
            [name, type, lat, long, ped, w, e, n, s] = v[:9]
            print "%s %s %s %s" % (name, type, lat, long)
            # This will create if not found
            #loc, c = Location.objects.get_or_create(organization=org, name=name)
            # Only update
            loc = Location.objects.get(organization=org, name=name)
            loc.type = type
            loc.latitude = lat
            loc.longitude = long
            loc.has_east = to_bool(e)
            loc.has_west = to_bool(w)
            loc.has_north = to_bool(n)
            loc.has_south = to_bool(s)
            loc.save()
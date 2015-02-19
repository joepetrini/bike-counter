import pytz
from django.utils import timezone
from django.conf import settings
from .models import Organization, Membership


class TimezoneMiddleware(object):
    def process_request(self, request):
        # TODO - set timezone at user/org level
        timezone.activate(pytz.timezone('US/Eastern'))

        # If set at a session scope
        #tzname = request.session.get('django_timezone')
        #if tzname:
        #    timezone.activate(pytz.timezone(tzname))
        #else:
        #    timezone.deactivate()


class RequireMembershipMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            return
        try:
            slug = view_kwargs['slug']
            m = Membership.objects.get(user=request.user, organization__slug=slug)
            request.current_org = slug
        except KeyError:
            try:
                m = Membership.objects.filter(user=request.user)[0]
            except IndexError:
                m = None
        # TODO - update current membership for multi-org on session
        request.member = m


def membership_context_processor(request):
    try:
        m = request.member
    except AttributeError:
        m = None
    d = {'member': m, 'version': settings.VERSION}
    return d
from .models import Organization, Membership


class RequireMembershipMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            return
        try:
            slug = view_kwargs['slug']
            m = Membership.objects.get(user=request.user, organization__slug=slug)
        except KeyError:
            try:
                m = Membership.objects.filter(user=request.user)[0]
            except IndexError:
                m = None
        request.member = m


def membership_context_processor(request):
    try:
        m = request.member
    except AttributeError:
        m = None
    return {'member': m,}
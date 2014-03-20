

class OrganizationMiddleware(object):
    """
    Not used yet.  Possible use to insert selected org into user's session
    """
    def process_request(self, request):
        request.organization = None

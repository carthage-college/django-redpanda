# -*- coding: utf-8 -*-

from redpanda.core.utils import get_coach


class UserTypeMiddleware(object):
    """Determine if the user faculty, staff, coach, admin."""

    def __init__(self, get_response):
        """One-time configuration and initialization."""
        self.get_response = get_response

    def __call__(self, request):
        """Code executed for each request/response after the view is called."""
        cid = request.user.id
        request.coaches = get_coach(request.user.id)
        response = self.get_response(request)
        return response

    '''
    def process_request(self, request):
        """Add the user type to the session."""
        request.coaches = True
        return

    def process_response(self, request, response):
        return response

    def process_template_response(self, request, response):
        """Check status and set the template context."""
        response.context_data['finaid'] = get_finaid(request.user.id)
        return response
    '''

import sys

from django.views.debug import technical_500_response
from raven.contrib.django.raven_compat.models import sentry_exception_handler


class UserBasedExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        sentry_exception_handler(request=request)

        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())

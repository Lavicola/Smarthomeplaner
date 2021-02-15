from django.utils.timezone import now
from .models import CustomUser
from datetime import date

class LastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            self.process_request(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self, request):
        # Update last visit time after request
        #last_visit = CustomUser.objects.filter(pk=request.user.email).values("last_visit").first()
        user = CustomUser.objects.get(pk=request.user.email)
        current_date = date.today()
        if(current_date > user.last_visit):
            user.last_visit = current_date
            user.save()
        return request
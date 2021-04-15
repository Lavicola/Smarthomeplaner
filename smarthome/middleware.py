from django.conf import settings
from django.conf.urls.i18n import is_language_prefix_patterns_used
from django.http import HttpResponseRedirect
from django.urls import get_script_prefix, is_valid_path
from django.utils import translation
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

# The Locale Middleware used for the Smarthomeplaner
class CustomLocaleMiddleware(MiddlewareMixin):
    """
    Decide in which Language the Content should be sent to Client.
    """
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        if(request.user.is_authenticated):            
            #user is logged in for the language we use the value stored in the database
            language = request.user.language_choice[0:2]
        else:
            #user is not logged in. We use the Accept Header value. If Language is not supported the default language english is used
            language = translation.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
        

    def process_response(self, request, response):
        language = translation.get_language()
        patch_vary_headers(response, ('Accept-Language',))
        response.setdefault('Content-Language', language)
        return response

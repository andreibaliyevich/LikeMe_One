from django.shortcuts import get_object_or_404
from .models import Region


class SetRegionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        if not request.session.get('user_region'):
            region = Region.objects.first()
            if region:
                request.session['user_region'] = region.slug
            else:
                request.session['user_region'] = ''
        
        response = self.get_response(request)
        
        return response

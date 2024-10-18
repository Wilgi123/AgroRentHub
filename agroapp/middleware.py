# agroapp/middleware.py

from django.utils.cache import add_never_cache_headers
from django.utils import timezone
from agroapp.models import CartItem

class DisableBrowserCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response

class RemoveExpiredCartItemsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = timezone.now()
        CartItem.objects.filter(start_date__lt=now).delete()
        response = self.get_response(request)
        return response
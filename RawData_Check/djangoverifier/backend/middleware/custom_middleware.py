from django.http import HttpRequest

class DisableCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.path == 'api/handle-info-click/<path:itemPath>/<str:arrival_date_time>':
            request._cache_update_cache = False

        response = self.get_response(request)
        return response
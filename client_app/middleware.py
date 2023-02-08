class SubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        subdomain = request.META.get('X_SUBDOMAIN')
        request.subdomain = subdomain
        response = self.get_response(request)
        return response

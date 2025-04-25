from django.http import HttpResponse

class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.build_absolute_uri().startswith('https://kienos-backend.onrender.com'):
            return HttpResponse({'Hello world'})

        response = self.get_response(request)
        return response

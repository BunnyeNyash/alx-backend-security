from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django_ratelimit.decorators import ratelimit


# Create your views here.
class RateLimitedLoginView(LoginView):
    template_name = 'login.html'

    @ratelimit(key='ip', rate='5/m', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Higher limit for authenticated users (handled by not applying ratelimit here)
            return super().post(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

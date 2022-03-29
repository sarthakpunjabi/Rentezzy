"""This holds all the custom decorators we are using for our project."""
from django.http import HttpResponseRedirect


def validate_user(user=None, redirect_url=None):
    """
    Check if the logged in user is a Customer or Agent.
    This translates to validate_user(user, redirect_url)(func).
    In our case func is a view method.
    """
    def decorator(func, *args, **kwargs):
        def inner(request):
            if request.user.type in user:
                return HttpResponseRedirect(redirect_url)
            return func(request, *args, **kwargs)

        return inner
    return decorator

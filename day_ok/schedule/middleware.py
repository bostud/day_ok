from django.core.exceptions import PermissionDenied


def authenticated(get_response):
    def middleware(request, *args, **kwargs):
        if request.user.is_authenticated:
            return get_response(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return middleware

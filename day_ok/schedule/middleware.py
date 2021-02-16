from django.core.exceptions import PermissionDenied


def authenticated(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            return get_response(request)
        else:
            raise PermissionDenied
    return middleware

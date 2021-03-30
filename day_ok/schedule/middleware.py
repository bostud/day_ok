from django.shortcuts import redirect


def authenticated(get_response):
    def middleware(request, *args, **kwargs):
        if request.user.is_authenticated:
            return get_response(request, *args, **kwargs)
        else:
            return redirect('dayok')
    return middleware

from django.shortcuts import loader
from django.http import HttpResponse, HttpRequest
# Create your views here.


def home_view(request: HttpRequest, *args, **kwargs):
    template = loader.get_template('day_ok/index.html')
    return HttpResponse(template.render(
        {
            'redirect_to_login': not request.user.is_authenticated,
        },
        request=request,
    ))


def page_not_found(request: HttpRequest, *args, **kwargs):
    template = loader.get_template('day_ok/errors/404.html')
    return HttpResponse(template.render(request=request))

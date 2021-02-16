from django.shortcuts import loader
from django.http import HttpResponse, HttpRequest
# Create your views here.
from .middleware import authenticated


@authenticated
def home_view(request: HttpRequest, *args, **kwargs):
    template = loader.get_template('schedule/base/base_cms.html')
    return HttpResponse(template.render(request=request))

from django.shortcuts import loader
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..middleware import authenticated


@authenticated
def home_view(request: HttpRequest, *args, **kwargs):
    template = loader.get_template('schedule/base/base_cms.html')
    return HttpResponse(template.render(request=request))


@authenticated
def reports(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


@authenticated
def about(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


@authenticated
def contacts(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


@authenticated
def logout(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')

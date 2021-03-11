from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from ..middleware import authenticated

from ..bl.base import get_source_statistics


@authenticated
def home_view(request: HttpRequest, *args, **kwargs):
    template = 'schedule/dashboard/base.html'
    context = dict(sources=get_source_statistics())
    return render(request, template, context)


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

from django.http import HttpRequest, HttpResponseRedirect
from ..middleware import authenticated


@authenticated
def classrooms(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


@authenticated
def classrooms_actions(request: HttpRequest, action: str, classroom_id: int):
    return HttpResponseRedirect('/schedule')

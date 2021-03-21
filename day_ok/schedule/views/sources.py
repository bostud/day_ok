from typing import Dict, Any
from ..middleware import authenticated
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from ..bl.sources import (
    all_sources, add_source,
    delete_source, get_source,
    change_source_name,
    delete_student_source,
    connect_student_to_source,
)
from ..forms.sources import (
    AddSource, DeleteSourceForm,
    ConnectStudentsForm, ChangeNameForm,
    DisconnectStudentForm,
    METHOD_DELETE, METHOD_EDIT
)


@authenticated
def sources(request: HttpRequest):
    ctx: Dict[Any, Any] = {}
    template_name = 'schedule/sources/base.html'

    def _view_all():
        ctx.update(sources=all_sources())
        ctx.update(form=AddSource())

    def _create():
        form = AddSource(request.POST)
        if form.is_valid():
            add_source(form.cleaned_data['name'])

    if request.method == 'POST':
        _create()

    _view_all()

    return render(request, template_name, ctx)


@authenticated
def source_actions(request: HttpRequest, source_id: int):
    ctx: Dict[Any, Any] = {}
    template_name = 'schedule/sources/view.html'

    if request.method == 'POST':
        form = DeleteSourceForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['method'] == METHOD_DELETE:
                delete_source(source_id)
    else:
        source = get_source(source_id)
        ctx.update(connect_students_form=ConnectStudentsForm({
            'students': source.free_students,
        }))
        ctx['source'] = source
        return render(request, template_name, ctx)
    return HttpResponseRedirect('/schedule/sources')


@authenticated
def source_actions_view(request: HttpRequest, source_id: int, action: str):
    def _connect_students():
        form = ConnectStudentsForm(request.POST)
        if form.is_valid():
            connect_student_to_source(
                students=form.cleaned_data['students'],
                source_id=source_id,
            )

    def _disconnect_student():
        form = DisconnectStudentForm(request.POST)
        if form.is_valid():
            delete_student_source(form.cleaned_data['student'])
            if form.cleaned_data['redirect_to'] == 'student_view':
                return f'/schedule/students/{form.cleaned_data["student"]}'

    def _change_name():
        form = ChangeNameForm(request.POST)
        if form.is_valid():
            change_source_name(source_id, form.cleaned_data['name'])

    actions = {
        'connect_students': _connect_students,
        'disconnect_student': _disconnect_student,
        'change_name': _change_name,
    }

    if func := actions.get(action):
        res = func()
        if res:
            return HttpResponseRedirect(res)

    return HttpResponseRedirect(f'/schedule/sources/{source_id}')

from typing import Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from ..middleware import authenticated
from ..bl.presence import (
    all_presence,
    get_all_presence,
    get_lessons_presence,
    edit_presence,
    delete_student_presence,
)
from ..forms.presence import (
    FilterPresenceForm,
    PresenceEditForm,
    PresenceDeleteForm,
)


@authenticated
def presence(request: HttpRequest):
    ctx: Dict[Any, Any] = {}
    template_name = 'schedule/presence/base.html'
    form_data = {}
    if request.method == 'GET':
        form = FilterPresenceForm(request.GET)
        if form.is_valid():
            form_data = form.cleaned_data
    ctx.update(presences=get_all_presence(**form_data))
    ctx.update(filter_form=FilterPresenceForm(form_data))

    return render(request, template_name, ctx)


@authenticated
def present_actions(request: HttpRequest, action: str, lessons_id: int):
    ctx: Dict[Any, Any] = {}
    template_name = 'schedule/presence/view.html'

    def _all_present():
        all_presence(lessons_id)
        if request.POST.get('redirect_to', '') == 'presence':
            return redirect('presence')

    def _edit_present():
        if request.method == 'POST':
            try:
                students = [
                    int(v) for v in request.POST.getlist('students', [])
                ]
            except:  # noqa
                students = []
            edit_presence(
                lessons_id,
                students,
            )

    def _view():
        pr = get_lessons_presence(lessons_id)
        ctx.update(presence=pr)
        free_students = list(
            set(pr.lessons.participants_list) - set(pr.participants.all())
        )
        edit_form = PresenceEditForm(
            initial={'students': free_students})
        ctx.update(edit_form=edit_form)
        ctx.update(free_students=free_students)

    def _delete_student_presence():
        if request.method == 'POST':
            form = PresenceDeleteForm(request.POST)
            if form.is_valid():
                delete_student_presence(lessons_id, **form.cleaned_data)
        return HttpResponseRedirect(f'/schedule/presence/{lessons_id}/edit')

    action_func = {
        'edit': _edit_present,
        'all': _all_present,
        'delete_student_presence': _delete_student_presence,
    }
    if f := action_func.get(action):
        res = f()
        if res:
            return res
        _view()
    else:
        ctx = {
            'errors': [f'Невірна дія: {action}']
        }
    return render(request, template_name, ctx)

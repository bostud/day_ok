from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect

from ..middleware import authenticated
from ..bl.students import (
    get_students, get_student, get_student_all_lessons,
    get_student_groups, get_student_invoices,
    get_student_future_lessons, add_source,
)
from ..forms.students import ChangeStudentStatusForm, AddSourceForm


@authenticated
def students(request: HttpRequest, *args, **kwargs):
    context: Dict[Any, Any] = dict()
    context['students'] = get_students()

    return render(request, 'schedule/students/base.html', context)


@authenticated
def students_actions(request: HttpRequest, student_id: int, action: str = None):
    context = dict()
    context['change_status_form'] = ChangeStudentStatusForm()
    context['add_source_form'] = AddSourceForm()

    def _lessons():
        context['lessons'] = get_student_future_lessons(student_id)
        context['all_lessons'] = get_student_all_lessons(student_id)
        context['view'] = action

    def _invoices():
        context['invoices'] = get_student_invoices(student_id)
        context['view'] = action

    def _groups():
        context['groups'] = get_student_groups(student_id)
        context['view'] = action

    def _add_source():
        if request.method == 'POST':
            form = AddSourceForm(request.POST)
            if form.is_valid():
                add_source(student_id, form.cleaned_data['source'])
        return f'/schedule/students/{student_id}'

    actions = {
        'lessons': _lessons,
        'invoices': _invoices,
        'groups': _groups,
        'add_source': _add_source,
    }

    if actions.get(action):
        res_url = actions[action]()
        if res_url:
            return HttpResponseRedirect(res_url)
    else:
        _lessons()
        context['view'] = 'lessons'

    context['student'] = get_student(student_id)
    return render(request, 'schedule/students/view.html', context)

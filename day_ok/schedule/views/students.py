from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest

from ..middleware import authenticated
from ..bl.students import (
    get_students, get_student, get_student_all_lessons,
    get_student_groups, get_student_invoices,
    get_student_future_lessons,
)
from ..forms.students import ChangeStudentStatusForm


@authenticated
def students(request: HttpRequest, *args, **kwargs):
    context: Dict[Any, Any] = dict()
    context['students'] = get_students()

    return render(request, 'schedule/students/base.html', context)


@authenticated
def students_actions(request: HttpRequest, student_id: int, action: str = None):
    context = dict(student=get_student(student_id))
    context['change_status_form'] = ChangeStudentStatusForm()

    def _lessons():
        context['lessons'] = get_student_future_lessons(student_id)
        context['all_lessons'] = get_student_all_lessons(student_id)

    def _invoices():
        context['invoices'] = get_student_invoices(student_id)

    def _groups():
        context['groups'] = get_student_groups(student_id)

    actions = {
        'lessons': _lessons,
        'invoices': _invoices,
        'groups': _groups,
    }

    if actions.get(action):
        actions[action]()
        context['view'] = action
    else:
        _lessons()
        context['view'] = 'lessons'

    return render(request, 'schedule/students/view.html', context)

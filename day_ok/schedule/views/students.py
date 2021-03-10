from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest

from ..middleware import authenticated
from ..bl.students import get_students, get_student, get_student_lessons
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
    context['next_lessons'] = get_student_lessons(student_id)

    return render(request, 'schedule/students/view.html', context)

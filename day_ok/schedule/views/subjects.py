from typing import Dict, Any
from django.shortcuts import render, redirect
from datetime import timedelta, datetime
from django.http import HttpRequest
from ..middleware import authenticated
from ..forms.subject import (
    SubjectForm,
)

from ..bl.subjects import (
    add_subject,
    get_subjects,
    delete_subject,
    edit_subject,
    get_subject,
)


@authenticated
def subject(request: HttpRequest):
    context: Dict[Any, Any] = {
        'form': SubjectForm(),
    }

    template_name = 'schedule/subject/base.html'

    def _view(**kwargs):
        context['subjects'] = get_subjects()

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            add_subject(**form.cleaned_data)
            return redirect('subject')
    _view()
    return render(request, template_name, context)


@authenticated
def subject_view(request: HttpRequest, subject_id: int):
    ctx: Dict[Any, Any] = {}
    template_name = 'schedule/subject/view.html'
    subject = get_subject(subject_id)

    def _edit():
        _subject = subject
        form = SubjectForm(request.POST)
        if form.is_valid():
            _subject = edit_subject(subject_id, **form.cleaned_data)
        return _view(_subject)

    def _view(_subject):
        duration = subject.duration_to_time
        data = {
            'name': subject.name,
            'hour': duration.tm_hour,
            'minute': duration.tm_min,
        } if _subject else {}
        ctx.update(form=SubjectForm(data=data))
        ctx.update(subject=_subject)
        return render(request, template_name, ctx)

    if request.method == 'GET':
        return _view(subject)
    elif request.method == 'POST':
        _edit()

    return redirect('subject')


@authenticated
def subject_delete(request: HttpRequest, subject_id: int):
    if request.method == 'POST':
        delete_subject(subject_id)
    return redirect('subject')

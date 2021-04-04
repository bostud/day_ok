from typing import Dict, Any
from django.shortcuts import render, redirect, Http404
from django.http import HttpRequest
from django.forms.models import model_to_dict
from ..middleware import authenticated
from ..forms.teachers import (
    TeacherLessonsColorForm,
    TeacherForm,
)

from ..bl.teachers import (
    teachers_objects,
    get_teacher,
    get_teacher_lessons_info,
    set_teacher_lessons_color,
    add_teacher,
    edit_teacher,
    prepare_date_fields,
    delete_teacher,
    unpin_teacher_subject,
)
from ..utils import (
    is_valid_period_format, create_datetime_start_from_period,
    create_datetime_end_period, get_year_month_periods, get_period,
    datetime_now_tz, create_datetime_start_period,
)


@authenticated
def teachers(request: HttpRequest, *args, **kwargs):
    context: Dict[Any, Any] = {}

    def _view():
        context.update(teachers=teachers_objects())
        context.update(form=TeacherForm())

    def _add():
        form = TeacherForm(request.POST)
        if form.is_valid():
            add_teacher(**form.cleaned_data)
        else:
            context.update(errors=form.errors)

    if request.method == 'POST':
        _add()

    _view()

    return render(request, 'schedule/teachers/base.html', context)


@authenticated
def teachers_view(request: HttpRequest, teacher_id: int):
    dt_now = datetime_now_tz()

    dt_start_period = create_datetime_start_period(dt_now)
    dt_end_period = create_datetime_end_period(dt_start_period)
    default_period = get_period(dt_now.year, dt_now.month)

    ctx: Dict[Any, Any] = {
        'periods': get_year_month_periods(),
        'selected_period': default_period,
    }
    template_name = 'schedule/teachers/view.html'

    def _edit():
        form = TeacherForm(request.POST)
        if form.is_valid():
            if not get_teacher(teacher_id):
                raise Http404("Викладач не існує")
            _teacher = edit_teacher(
                teacher_id,
                **form.cleaned_data,
            )
        _view()

    def _view():
        period = request.GET.get('period')
        dt_start, dt_end = None, None
        if period and is_valid_period_format(period):
            dt_start = create_datetime_start_from_period(period)
            dt_end = create_datetime_end_period(dt_start)
            ctx.update(selected_period=period)
        ctx.update(
            lessons_reports=get_teacher_lessons_info(
                teacher_id,
                dt_start or dt_start_period,
                dt_end or dt_end_period
            )
        )
        teacher = get_teacher(teacher_id)
        if not teacher:
            raise Http404("Викладач не існує")

        data = model_to_dict(teacher)
        prepare_date_fields(data)
        ctx.update(teacher=teacher)
        ctx.update(form=TeacherForm(data=data))

    if request.method == 'POST':
        _edit()
    elif request.method == 'GET':
        if res := _view():
            return res
    else:
        return redirect('teachers')

    return render(request, template_name, ctx)


@authenticated
def set_teacher_lessons_style(request: HttpRequest, teacher_id: int):
    if request.method == 'POST':
        form = TeacherLessonsColorForm(request.POST)
        if form.is_valid():
            _teacher = set_teacher_lessons_color(
                teacher_id,
                **form.cleaned_data,
            )
    return redirect('teachers_actions', teacher_id)


@authenticated
def teacher_delete(request: HttpRequest, teacher_id: int):
    if request.method == 'POST':
        delete_teacher(teacher_id)
    return redirect('teachers')


@authenticated
def unpin_subject(request: HttpRequest, teacher_id: int):
    if request.method == 'POST':
        unpin_teacher_subject(
            teacher_id,
            request.POST.get('subject_id', -1),
        )
    return redirect('teachers_actions', teacher_id)

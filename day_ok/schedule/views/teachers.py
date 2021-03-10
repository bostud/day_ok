from typing import Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest
from ..middleware import authenticated
from ..forms.teachers import TeacherLessonsColorForm

from ..bl.teachers import (
    teachers_objects, get_teacher, get_teacher_lessons_info,
    set_teacher_lessons_color,
)
from ..utils import (
    is_valid_period_format, create_datetime_start_from_period,
    create_datetime_end_period, get_year_month_periods, get_period,
    datetime_now_tz, create_datetime_start_period,
)


@authenticated
def teachers(request: HttpRequest, *args, **kwargs):
    context = {
        'teachers': teachers_objects(),
    }
    return render(request, 'schedule/teachers/base.html', context)


@authenticated
def teachers_actions(request: HttpRequest, action: str, teacher_id: int):
    dt_now = datetime_now_tz()

    dt_start_period = create_datetime_start_period(dt_now)
    dt_end_period = create_datetime_end_period(dt_start_period)
    default_period = get_period(dt_now.year, dt_now.month)

    ctx: Dict[Any, Any] = {
        'periods': get_year_month_periods(),
        'teacher': get_teacher(teacher_id),
        'selected_period': default_period,
    }
    template_name = 'schedule/teachers/view.html'

    def _edit():
        pass

    def _delete():
        pass

    def _view():
        if request.method == 'GET':
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
        elif request.method == 'POST':
            form = TeacherLessonsColorForm(request.POST)
            if form.is_valid():
                teacher = set_teacher_lessons_color(
                    color=form.cleaned_data['color'],
                    teacher_id=teacher_id,
                )
                dt_start = create_datetime_start_from_period(default_period)
                dt_end = create_datetime_end_period(dt_start)
                if teacher:
                    ctx.update(teacher=teacher)
                ctx.update(
                    lessons_reports=get_teacher_lessons_info(
                        teacher_id, dt_start, dt_end
                    )
                )

    actions_func = {
        'view': _view,
    }

    if actions_func.get(action):
        actions_func[action]()
    else:
        return redirect('lessons')

    return render(request, template_name, ctx)

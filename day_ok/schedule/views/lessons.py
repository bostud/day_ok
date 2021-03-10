from typing import Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest
from ..middleware import authenticated
from datetime import datetime, timedelta
from django.utils.timezone import now

from ..forms.lessons import (
    LessonsByClassRoomForm,
    AddLessonsForm, LessonsByDayForm,
    EditLessonsForm, FilterLessonsForm,
)
from ..models import ClassRoom
from ..bl.lessons import (
    get_weekly_classroom_lessons_by_classroom,
    prepare_add_lessons_form_data,
    add_lessons_from_form,
    get_weekly_classroom_lessons_by_day,
    prepare_edit_lessons_form_data,
    delete_lessons,
    edit_lessons_from_form,
    get_lessons_data_by_filter_form,
    get_lessons_data_for_teachers,
)
from ..utils import (
    get_weekday_number, get_weekday_name,
    get_day_time_periods, get_live_time_period
)


@authenticated
def lessons_view(request: HttpRequest, show_type: str, *args, **kwargs):
    if show_type == 'day':
        landing_form = LessonsByDayForm
    elif show_type == 'classroom':
        landing_form = LessonsByClassRoomForm
    elif show_type == 'teachers':
        landing_form = LessonsByDayForm
    else:
        landing_form = FilterLessonsForm

    context: Dict[Any, Any] = {
        'form': landing_form(),
        'show_type': show_type,
    }
    dt_now = now()

    def _fill_context_by_form_data_for_classroom(dt, cls_room):
        weekly_schedule = get_weekly_classroom_lessons_by_classroom(
            cls_room,
            dt
        )
        context['lessons_date_to'] = (
                dt + timedelta(days=6)
        ).strftime('%d.%m.%Y')
        context['selected_classroom'] = (
            ClassRoom.objects.get(id=cls_room).name
        )
        week_days_names = ([
            get_weekday_name(get_weekday_number(
                datetime.strptime(dt, '%d.%m.%Y')))
            for dt in weekly_schedule
        ])
        context['total_schedule'] = list(zip(
            week_days_names,
            weekly_schedule.values(),
            weekly_schedule.keys(),
        ))

    def _fill_context_by_form_data_for_date(dt: datetime):
        day_schedule = get_weekly_classroom_lessons_by_day(dt)
        context['total_schedule'] = day_schedule.items()

    def _fill_context_by_form_filter(frm: FilterLessonsForm):
        day_schedule = get_lessons_data_by_filter_form(frm)
        context['total_schedule'] = day_schedule

    def _fill_context_for_form_teachers(dt: datetime):
        day_schedule = get_lessons_data_for_teachers(dt)
        res = [teacher for teacher in day_schedule]
        context.update(form=LessonsByDayForm({'date': dt.strftime('%d.%m.%Y')}))
        context['total_schedule'] = res
        context['tomorrow_date'] = now() + timedelta(days=1)
        context['yesterday_date'] = now() - timedelta(days=1)
        context['today_date'] = now()
        context['live_period'] = get_live_time_period()
        context['time_periods'] = get_day_time_periods()

    if request.method == 'GET':
        form = landing_form(request.GET)
        if form.is_valid():
            if show_type == 'day':
                date_from = form.cleaned_data['date']
                _fill_context_by_form_data_for_date(date_from)
            elif show_type == 'classroom':
                classroom = int(form['classroom'].value())
                date_from = form.cleaned_data['date_from']
                _fill_context_by_form_data_for_classroom(date_from, classroom)
            elif show_type == 'teachers':
                date_from = form.cleaned_data['date']
                _fill_context_for_form_teachers(date_from)
            else:
                date_from = form.cleaned_data['date_from']
                _fill_context_by_form_filter(form)
            context['lessons_date_from'] = date_from.strftime('%d.%m.%Y')
        elif show_type == 'day':
            _fill_context_by_form_data_for_date(dt_now)
            context['lessons_date_from'] = dt_now.strftime('%d.%m.%Y')
        elif show_type == 'teachers':
            _fill_context_for_form_teachers(now())
        elif show_type == 'filter':
            form = FilterLessonsForm(data={'date_from': dt_now})
            form.is_valid()
            _fill_context_by_form_filter(form)

    return render(request, 'schedule/lessons/main.html', context)


@authenticated
def add_lessons(request: HttpRequest, *args, **kwargs):
    context = {
        'form': AddLessonsForm(),
        'create_lessons': True,
    }
    context.update(**prepare_add_lessons_form_data())
    if request.method == 'POST':
        form = AddLessonsForm(request.POST)
        if form.is_valid():
            new_lessons_count = add_lessons_from_form(form)
            context['new_lessons'] = new_lessons_count

    return render(request, 'schedule/lessons/actions.html', context)


@authenticated
def lessons_actions(request: HttpRequest, action: str, lessons_id: int):
    ctx = {}
    template_name = 'schedule/lessons/actions.html'

    def _edit():
        ctx.update(edit_lessons=True)
        ctx.update(**prepare_edit_lessons_form_data(lessons_id))
        ctx.update(**prepare_add_lessons_form_data())
        if request.method == 'POST':
            edit_form = EditLessonsForm(request.POST)
            if edit_form.is_valid():
                edit_lessons_from_form(form=edit_form, lessons_id=lessons_id)
                ctx.update(edited_lessons=True)
                ctx.update(**prepare_edit_lessons_form_data(lessons_id))
                return redirect('lessons_action', 'edit', lessons_id)

    def _delete():
        ctx.update(delete_lessons=True)
        ctx.update(**prepare_edit_lessons_form_data(lessons_id))
        ctx.update(**prepare_add_lessons_form_data())
        if request.method == 'POST':
            edit_form = EditLessonsForm(request.POST)
            edit_form.is_valid()
            delete_lessons(lessons_id, edit_form.cleaned_data['change_all'])
            return redirect('lessons', show_type='filter')

    def _view():
        ctx.update(view_lessons=True)
        ctx.update(**prepare_add_lessons_form_data())
        ctx.update(**prepare_edit_lessons_form_data(lessons_id))

    actions_func = {
        'edit': _edit,
        'delete': _delete,
        'view': _view,
    }

    if actions_func.get(action):
        res = actions_func[action]()
        if res:
            return res

    return render(request, template_name, ctx)

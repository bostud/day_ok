from typing import Dict, Any
from django.shortcuts import loader, render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
# Create your views here.
from .middleware import authenticated
from datetime import datetime, timedelta

from .forms import (
    LessonsByClassRoomForm, EventsForm,
    AddLessonsForm, LessonsByDayForm,
    EditLessonsForm,
)
from .models import ClassRoom
from .controllers.lessons import (
    get_weekly_class_room_lessons_by_classroom,
    all_presence,
    prepare_add_lessons_form_data,
    add_lessons_from_form,
    get_weekly_class_room_lessons_by_day,
    prepare_edit_lessons_form_data,
    delete_lessons,
    edit_lessons_from_form,
)
from .controllers.events import (
    get_weekly_class_room_events_by_day,
)
from .utils import get_weekday_number, get_weekday_name


@authenticated
def home_view(request: HttpRequest, *args, **kwargs):
    template = loader.get_template('schedule/base/base_cms.html')
    return HttpResponse(template.render(request=request))


@authenticated
def lessons_view(request: HttpRequest, show_type: str, *args, **kwargs):
    if show_type == 'day':
        landing_form = LessonsByDayForm
    else:
        landing_form = LessonsByClassRoomForm

    context: Dict[Any, Any] = {
        'form': landing_form(),
        'show_type': show_type,
    }

    def _fill_context_by_form_data_for_classroom(dt, cls_room):
        weekly_schedule = get_weekly_class_room_lessons_by_classroom(
            cls_room,
            dt
        )
        context['lessons_date_to'] = (
                dt + timedelta(days=6)
        ).strftime('%d.%m.%Y')
        context['selected_class_room'] = (
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
        day_schedule = get_weekly_class_room_lessons_by_day(dt)
        context['total_schedule'] = day_schedule.items()

    if request.method == 'GET':
        form = landing_form(request.GET)
        if form.is_valid():
            if show_type == 'day':
                date_from = form.cleaned_data['date']
                _fill_context_by_form_data_for_date(date_from)
            else:
                class_room = int(form['class_room'].value())
                date_from = datetime.strptime(
                    form['date_from'].value(),
                    '%m/%d/%Y'
                ).date()
                _fill_context_by_form_data_for_classroom(date_from, class_room)
            context['lessons_date_from'] = date_from.strftime('%d.%m.%Y')
        elif show_type == 'day':
            _fill_context_by_form_data_for_date(datetime.today())
            context['lessons_date_from'] = datetime.today().strftime('%d.%m.%Y')

    return render(request, 'schedule/lessons/lessons_schedule.html', context)


@authenticated
def events_view(request: HttpRequest, *args, **kwargs):
    context: Dict[Any, Any] = {
        'form': EventsForm(),
    }

    def _fill_context_by_form_data(dt, cls_room):
        weekly_schedule = get_weekly_class_room_events_by_day(
            cls_room,
            dt
        )
        context['events_date_from'] = dt.strftime('%d.%m.%Y')
        context['events_date_to'] = (
                dt + timedelta(days=6)
        ).strftime('%d.%m.%Y')
        context['selected_class_room_name'] = (
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

    if request.method == 'GET':
        form = EventsForm(request.GET)
        if form.is_valid():
            class_room = int(form['class_room'].value())
            date_from = datetime.strptime(
                form['date_from'].value(),
                '%m/%d/%Y'
            ).date()
            _fill_context_by_form_data(date_from, class_room)

    return render(request, 'schedule/events.html', context)


@authenticated
def present_actions(request: HttpRequest, action: str, lessons_id: int):
    ctx = {}
    template_name = 'schedule/lessons/lessons_schedule.html'

    def _all_present():
        all_presence(lessons_id)
        return HttpResponseRedirect(
            '/schedule/' + str(request.headers['Referer'].split('/')[-1])
        )

    def _edit_present():
        pass

    def _clean_present():
        pass

    action_func = {
        'edit': _edit_present,
        'all': _all_present,
        'clean': _clean_present,
    }
    if f := action_func.get(action):
        f()
    else:
        ctx = {
            'errors': [f'Невірна дія: {action}']
        }
    return render(request, template_name, ctx)


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

    return render(request, 'schedule/lessons/lessons_actions.html', context)


@authenticated
def lessons_actions(request: HttpRequest, action: str, lessons_id: int):
    ctx = {}
    template_name = 'schedule/lessons/lessons_actions.html'

    def _edit():
        ctx.update(edit_lessons=True)
        if request.method == 'GET':
            ctx.update(**prepare_edit_lessons_form_data(lessons_id))
        elif request.method == 'POST':
            edit_form = EditLessonsForm(request.POST)
            if edit_form.is_valid():
                edit_lessons_from_form(form=edit_form)

    def _delete():
        ctx.update(delete_lessons=True)
        delete_lessons(lessons_id, delete_all=False)

    def _view():
        pass

    actions_func = {
        'edit': _edit,
        'delete': _delete,
        'view': _view,
    }

    if actions_func.get(action):
        actions_func[action]()
    else:
        return redirect('lessons_by_day')

    return render(request, template_name, ctx)


@authenticated
def add_class_room(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


@authenticated
def add_event(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule/events')


@authenticated
def reports(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


@authenticated
def event_actions(request: HttpRequest, action: str, event_id: int):
    ctx = {}
    template_name = ''

    def _edit():
        pass

    def _delete():
        pass

    def _view():
        pass

    actions_func = {
        'edit': _edit,
        'delete': _delete,
        'view': _view,
    }

    if actions_func.get(action):
        actions_func[action]()
    else:
        return redirect('lessons_by_day')

    return render(request, template_name, ctx)

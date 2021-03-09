from typing import Dict, Any
from django.shortcuts import loader, render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .middleware import authenticated
from datetime import datetime, timedelta
from django.utils.timezone import now

from .forms.lessons import (
    LessonsByClassRoomForm,
    AddLessonsForm, LessonsByDayForm,
    EditLessonsForm, FilterLessonsForm,
)
from .forms.events import FilterEventsForm
from .forms.teachers import TeacherLessonsColorForm
from .forms.invoices import (
    FilterInvoiceFrom, prepare_cleaned_data_to_form,
    CreateInvoiceForm, ChangeInvoiceStatusForm
)
from .models import ClassRoom
from .bl.lessons import (
    get_weekly_classroom_lessons_by_classroom,
    all_presence,
    prepare_add_lessons_form_data,
    add_lessons_from_form,
    get_weekly_classroom_lessons_by_day,
    prepare_edit_lessons_form_data,
    delete_lessons,
    edit_lessons_from_form,
    get_lessons_data_by_filter_form,
    get_lessons_data_for_teachers,
)
from .bl.events import (
    get_events_data_by_filter_form,
    get_filter_by_description
)
from .bl.groups import (
    groups_objects, get_group, get_group_info_by_period
)

from .bl.teachers import (
    teachers_objects, get_teacher, get_teacher_lessons_info,
    set_teacher_lessons_color,
)
from .bl.invoices import (
    total_pages, filter_invoices, create_invoice,
    get_invoice_change_log, get_invoice, change_invoice_status
)
from .utils import (
    get_weekday_number, get_weekday_name,
    is_valid_period_format, create_datetime_start_from_period,
    create_datetime_end_period, get_year_month_periods, get_period,
    datetime_now_tz, create_datetime_start_period,
    get_day_time_periods,
)


@authenticated
def home_view(request: HttpRequest, *args, **kwargs):
    template = loader.get_template('schedule/base/base_cms.html')
    return HttpResponse(template.render(request=request))


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
        context['total_schedule'] = res
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
def events_view(request: HttpRequest, *args, **kwargs):
    context: Dict[Any, Any] = {
        'form': FilterEventsForm(),
    }

    def _fill_context_by_form_data(fr: FilterEventsForm):
        events_data, is_empty = get_events_data_by_filter_form(fr)
        desc = get_filter_by_description(fr)
        context['filter_by_text'] = desc
        if not is_empty:
            context['total_schedule'] = events_data

    if request.method == 'GET':
        form = FilterEventsForm(request.GET)
        if form.is_valid():
            _fill_context_by_form_data(form)

    return render(request, 'schedule/events/base.html', context)


@authenticated
def present_actions(request: HttpRequest, action: str, lessons_id: int):
    ctx = {}
    template_name = 'schedule/lessons/main.html'

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


@authenticated
def classrooms(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


@authenticated
def classrooms_actions(request: HttpRequest, action: str, classroom_id: int):
    return HttpResponseRedirect('/schedule')


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
        return redirect('lessons')

    return render(request, template_name, ctx)


@authenticated
def groups(request: HttpRequest, *args, **kwargs):
    context = {
        'groups': groups_objects(),
    }
    return render(request, 'schedule/groups/base.html', context)


@authenticated
def groups_actions(request: HttpRequest, action: str, group_id: int):
    ctx: Dict[Any, Any] = {
        'periods': get_year_month_periods(),
        'selected_period': None
    }
    template_name = 'schedule/groups/view.html'

    def _edit():
        pass

    def _delete():
        pass

    def _view():
        if request.method == 'GET':
            period = request.GET.get('period')
            if period and is_valid_period_format(period):
                dt_start = create_datetime_start_from_period(period)
                dt_end = create_datetime_end_period(dt_start)
                ctx.update(selected_period=period)
                ctx.update(
                    group=get_group_info_by_period(group_id, dt_start, dt_end)
                )
            else:
                ctx.update(group=get_group(group_id))

    actions_func = {
        'view': _view,
    }

    if actions_func.get(action):
        actions_func[action]()
    else:
        return redirect('lessons')

    return render(request, template_name, ctx)


@authenticated
def students(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


@authenticated
def students_actions(request: HttpRequest, action: str, student_id: int):
    return HttpResponseRedirect('/schedule')


@authenticated
def about(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


@authenticated
def contacts(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


@authenticated
def logout(request: HttpRequest, *args, **kwargs):
    return HttpResponseRedirect('/schedule')


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


@authenticated
def invoices(request: HttpRequest, *args, **kwargs):
    page = request.GET.get('page', 0)
    if all([l.isdigit() for l in str(page)]):
        page = int(page)
    else:
        page = 0
    pages = total_pages()
    context = {
        'prev_page': page - 1,
        'pages': total_pages(),
        'current_page': page,
        'next_page': page + 1 if page + 1 < max(pages) else page,
        'create_form': CreateInvoiceForm(),
    }
    form = FilterInvoiceFrom(request.GET)
    if form.is_valid():
        form_data = prepare_cleaned_data_to_form(form)
        context.update(filter_form=FilterInvoiceFrom(
            form_data
        ))
        context.update(invoices=filter_invoices(**form.cleaned_data))
    else:
        context.update(filter_form=FilterInvoiceFrom({
            'date_valid_from': now().strftime('%d.%m.%Y')
        }))
        context.update(invoices=filter_invoices(date_valid_from=now().date()))

    return render(request, 'schedule/invoices/base.html', context)


@authenticated
def invoices_add(request: HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        form = CreateInvoiceForm(request.POST)
        if form.is_valid():
            create_invoice(request, **form.cleaned_data)
    return HttpResponseRedirect('/schedule/invoices')


@authenticated
def invoices_actions(request: HttpRequest, action: str, invoice_id: int):

    context: Dict[Any, Any] = {}
    errors = []

    def __error_wrong_action():
        return f'Невірна дія над рахунком: {action} - {invoice_id}'

    def __error_not_found():
        return f'Рахунок не знайдено: {invoice_id}'

    def trow_error(*errors):
        context.update(errors=[*errors])
        return render(request, 'schedule/invoices/base.html', context)

    def _view():
        invoice = get_invoice(int(invoice_id))
        if invoice:
            change_log = get_invoice_change_log(invoice)
            context.update(invoice=invoice)
            context.update(history_records=change_log)
            context.update(change_status_form=ChangeInvoiceStatusForm())
            return render(request, 'schedule/invoices/view.html', context)
        else:
            errors.append(__error_not_found())

    def _paid():
        from .models import Invoice
        if request.method == 'POST':
            invoice = get_invoice(int(invoice_id))
            if invoice:
                change_invoice_status(
                    request,
                    invoice,
                    new_status=Invoice.Status.PAID,
                )
        return HttpResponseRedirect('/schedule/invoices')

    _actions = {
        'view': _view,
        'paid': _paid,
    }

    if action not in _actions:
        trow_error(__error_wrong_action())

    res = _actions[action]()
    if res:
        return res

    context.update(errors=errors)
    context.update(invoices=filter_invoices())
    context.update(info_posts=['Сервіс на епаті розробки, натисніть "Очистити"'])
    return render(request, 'schedule/invoices/base.html', context)


@authenticated
def invoices_change_status(request: HttpRequest, invoice_id: int):
    if request.method == 'POST':
        form = ChangeInvoiceStatusForm(request.POST)
        if form.is_valid():
            invoice = get_invoice(int(invoice_id))
            if invoice:
                change_invoice_status(
                    request=request,
                    invoice=invoice,
                    new_status=form.cleaned_data['status']
                )
                return HttpResponseRedirect(
                    f'/schedule/invoices/view/{invoice_id}'
                )
    return HttpResponseRedirect('/schedule/invoices')

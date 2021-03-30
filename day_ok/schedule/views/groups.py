from typing import Dict, Any
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import HttpRequest
from ..middleware import authenticated
from ..bl.groups import (
    groups_objects,
    get_group,
    get_group_info_by_period,
    add_group,
    edit_group,
    delete_group,
    unpin_student,
)
from ..forms.group import (
    GroupForm,
)
from ..utils import (
    is_valid_period_format, create_datetime_start_from_period,
    create_datetime_end_period, get_year_month_periods, DATE_START_PERIODS,
    datetime_now_tz as now,
)


@authenticated
def groups(request: HttpRequest, *args, **kwargs):
    context = {
        'form': GroupForm(),
    }

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            _, error = add_group(**form.cleaned_data)
            context.update(error=error)
    context.update(groups=groups_objects())
    return render(request, 'schedule/groups/base.html', context)


@authenticated
def groups_actions(request: HttpRequest, group_id: int):
    ctx: Dict[Any, Any] = {
        'periods': get_year_month_periods(),
        'selected_period': None
    }
    template_name = 'schedule/groups/view.html'

    def _edit():
        form = GroupForm(request.POST)
        if form.is_valid():
            edit_group(group_id, **form.cleaned_data)

    def _view():
        period = request.GET.get('period')
        if period and is_valid_period_format(period):
            dt_start = create_datetime_start_from_period(period)
            dt_end = create_datetime_end_period(dt_start)
            ctx.update(selected_period=period)
        else:
            dt_start = DATE_START_PERIODS
            dt_end = now()
        ctx.update(
            group_data=get_group_info_by_period(group_id, dt_start, dt_end)
        )
        group = get_group(group_id)
        if group:
            ctx.update(group=group)
            data = model_to_dict(group)
            form = GroupForm(
                data=data,
            )
            form.fields['students'].choices = [(s.id, str(s)) for s in group.students_not_in_group]  # noqa
            ctx.update(form=form)
    if request.method == 'POST':
        _edit()

    _view()

    return render(request, template_name, ctx)


@authenticated
def group_delete(request: HttpRequest, group_id: int):
    if request.method == 'POST':
        delete_group(group_id)
    return redirect('groups')


@authenticated
def group_unpin_student(request: HttpRequest, group_id: int):
    if request.method == 'POST' and request.POST.get('student'):
        unpin_student(
            group_id,
            int(request.POST.get('student', -1)),
        )
    return redirect('groups_actions', group_id)

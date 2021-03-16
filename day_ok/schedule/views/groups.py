from typing import Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest
from ..middleware import authenticated
from ..bl.groups import (
    groups_objects, get_group, get_group_info_by_period
)
from ..utils import (
    is_valid_period_format, create_datetime_start_from_period,
    create_datetime_end_period, get_year_month_periods, DATE_START_PERIODS,
    datetime_now_tz as now,
)


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
            else:
                dt_start = DATE_START_PERIODS
                dt_end = now()
            ctx.update(
                group_data=get_group_info_by_period(group_id, dt_start, dt_end)
            )
            ctx.update(group=get_group(group_id))

    actions_func = {
        'view': _view,
    }

    if actions_func.get(action):
        actions_func[action]()
    else:
        return redirect('lessons')

    return render(request, template_name, ctx)

from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest
from ..middleware import authenticated
from ..bl.finance import get_teachers_month_statistics
from ..forms.finance import TeacherSalaryStatForm


TEMPLATE = 'schedule/finance/base.html'


@authenticated
def finance(request: HttpRequest):
    ctx: Dict[Any, Any] = dict()
    date_start = None
    date_end = None
    if request.method == 'GET':
        form = TeacherSalaryStatForm(request.GET)
        if form.is_valid():
            date_start = form.cleaned_data['date_start']
            date_end = form.cleaned_data['date_end']
            ctx.update(filter_form=TeacherSalaryStatForm({
                'date_start': date_start.strftime('%d.%m.%Y'),
                'date_end': date_end.strftime('%d.%m.%Y'),
            }))

    teachers_month_statistics = get_teachers_month_statistics(
        date_start,
        date_end
    )
    if not ctx.get('filter_form'):
        ctx.update(filter_form=TeacherSalaryStatForm())
    ctx.update(teachers_month_statistics=list(teachers_month_statistics))
    return render(request, TEMPLATE, ctx)

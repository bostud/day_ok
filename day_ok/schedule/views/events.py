from typing import Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest
from ..middleware import authenticated
from ..forms.events import FilterEventsForm
from ..bl.events import (
    get_events_data_by_filter_form,
    get_filter_by_description
)


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

from typing import Dict, Any
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponseRedirect
from ..middleware import authenticated
from ..forms.events import (
    FilterEventsForm,
    EventForm,
    EventLocationForm,
    EventParticipantDeleteForm,
)

from ..bl.events import (
    add_event,
    get_events,
    add_event_location,
    delete_event,
    edit_event,
    get_event,
    delete_event_participant,
)


@authenticated
def events(request: HttpRequest):
    context: Dict[Any, Any] = {
        'form': EventForm(),
        'location_form': EventLocationForm(),
        'filter_form': FilterEventsForm(),
    }

    template_name = 'schedule/events/base.html'

    def _view_all(**kwargs):
        context['events'] = get_events(**kwargs)

    if request.method == 'GET':
        form = FilterEventsForm(request.GET)
        if form.is_valid():
            context.update(events=get_events(**form.cleaned_data))
            context.update(filter_form=form)
    else:
        form = EventForm(request.POST)
        if form.is_valid():
            add_event(**form.cleaned_data)
        _view_all()
    return render(request, template_name, context)


@authenticated
def event_actions(request: HttpRequest, event_id: int,  action: str):
    ctx: Dict[Any, Any] = {}
    template_name = 'schedule/events/view.html'
    event = get_event(event_id)

    def _edit():
        _event = event
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                _event = edit_event(event_id, **form.cleaned_data)
        return _view(_event)

    def _delete():
        delete_event(event_id)

    def _view(_event):
        data = model_to_dict(_event) if _event else {}
        if data:
            data['date_of_event'] = data['date_of_event'].strftime('%d.%m.%Y')
        ctx.update(edit_form=EventForm(data=data))
        ctx.update(event=_event)
        return render(request, template_name, ctx)

    def _delete_participant():
        _event = event
        if request.method == 'POST':
            form = EventParticipantDeleteForm(request.POST)
            if form.is_valid():
                _event = delete_event_participant(event_id, **form.cleaned_data)
        return _view(_event)

    actions_func = {
        'edit': _edit,
        'delete': _delete,
        'view': _view,
        'delete_participant': _delete_participant,
    }

    if actions_func.get(action):
        res = actions_func[action]()
        if res:
            return res

    return redirect('events')


@authenticated
def event_location(request: HttpRequest):
    if request.method == 'POST':
        form = EventLocationForm(request.POST)
        if form.is_valid():
            add_event_location(**form.cleaned_data)
    return HttpResponseRedirect('/schedule/events')

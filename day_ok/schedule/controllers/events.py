from typing import List
from ..utils import get_days_from_date, get_weekday_name_by_date
from ..forms import FilterEventsForm
from ..models import (
    ClassRoom, Student, Event
)


def _group_events_by_classrooms(
    events: List[Event],
    classrooms: List[ClassRoom],
) -> dict:
    result = {}
    for cl in classrooms:
        data = list(filter(lambda x: x.class_room == cl, events))
        if data:
            result[cl.id] = data
    return result


def get_events_data_by_filter_form(form: FilterEventsForm):
    add_days = form.cleaned_data['additional_days']  # noqa
    dt_list = get_days_from_date(
        form.cleaned_data['date_from'],
        int(add_days if add_days else 7),
    )
    result = []
    classrooms = ClassRoom.objects.all()
    query_filter = {}
    if form.cleaned_data['class_rooms']:
        objs = [
            ClassRoom.objects.get(id=int(v))
            for v in form.cleaned_data['class_rooms']
        ]
        query_filter.update(class_room__in=objs)
    if form.cleaned_data['students']:
        objs = [
            Student.objects.get(id=int(v))
            for v in
            form.cleaned_data['students']
        ]
        query_filter.update(participants__in=objs)
    is_empty = True
    for dt in dt_list:
        query_filter.update(date_of_event=dt)
        q = Event.objects.filter(**query_filter).order_by('time_start')
        data = _group_events_by_classrooms(q.all(), classrooms)
        cls_rms = list(filter(lambda x: x.id in data.keys(), classrooms))
        result.append((
            dt,
            get_weekday_name_by_date(dt),
            tuple(zip(cls_rms, data.values()))
        ))
        if q:
            is_empty = False
    return result, is_empty


def get_filter_by_data(form: FilterEventsForm):
    class_rooms = [
        ClassRoom.objects.get(id=int(v))
        for v in form.cleaned_data['class_rooms']
    ]
    students = [
        Student.objects.get(id=int(v))
        for v in
        form.cleaned_data['students']
    ]
    return {
        'class_rooms': class_rooms,
        'students': students,
        'date': form.cleaned_data['date_from'],
        'additional_days': form.cleaned_data['additional_days']
    }


def get_filter_by_description(form: FilterEventsForm):
    data = get_filter_by_data(form)
    date = data['date'].strftime('%d.%m.%Y') if data.get('date') else '---'
    return f"Аудиторії: " \
           f"{'/'.join([o.name for o in data.get('class_rooms', [])])}, " \
           f"Учасники: " \
           f"{'/'.join([o.full_name for o in data.get('students', [])])}, " \
           f"Дата: {date}, " \
           f"Додаткові дні: {data.get('additional_days')}"

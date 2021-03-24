from typing import List, Optional
from ..models import (
    Student, Event, EventLocation
)
from django.forms.models import model_to_dict
from datetime import datetime


def add_event(
    name: str,
    date_of_event: datetime.date,
    time_start: datetime.time,
    time_end: datetime.time,
    location: int,
    participants: List[int],
) -> Optional[Event]:
    location = EventLocation.objects.filter(id=int(location)).first()
    if location:
        e = Event(
            name=name,
            date_of_event=date_of_event,
            time_start=time_start,
            time_end=time_end,
            location=location,
        )
        e.save()
        e.participants.add(
            *Student.objects.filter(id__in=[int(p) for p in participants]).all()
        )
        e.save()
        return e
    return None


def get_events(**kwargs) -> List[Optional[Event]]:
    query_filter = {}
    if location := kwargs.get('location'):
        query_filter.update(
            location__in=location if isinstance(location, list) else [location],
        )
    if student := kwargs.get('student'):
        student = student if isinstance(student, list) else [student]
        query_filter.update(
            participants__in=student,
        )
    if date_from := kwargs.get('date_from'):
        query_filter.update(
            date_of_event__gte=date_from
        )
    if date_until := kwargs.get('date_until'):
        query_filter.update(
            date_of_event__lte=date_until
        )
    return Event.objects.filter(**query_filter).all()


def add_event_location(
    location: str,
) -> Optional[EventLocation]:
    event_location = EventLocation.objects.filter(location=location).first()
    if not event_location:
        event_location = EventLocation(location=location)
        event_location.save()

    return event_location


def delete_event(
    event: int,
) -> Optional[dict]:
    e = Event.objects.filter(id=event).first()
    if e:
        data = model_to_dict(e)
        e.delete()
        return data
    return None


def edit_event(
    event_id: int,
    name: str,
    date_of_event: datetime.date,
    time_start: datetime.time,
    time_end: datetime.time,
    location: int,
    participants: List[int],
) -> Optional[Event]:
    event = Event.objects.filter(id=event_id).first()
    location = EventLocation.objects.filter(id=int(location)).first()
    if event and location:
        event.name = name
        event.date_of_event = date_of_event
        event.time_start = time_start
        event.time_end = time_end
        event.location = location
        event.participants.add(
            *Student.objects.filter(id__in=[int(p) for p in participants]).all()
        )
        event.save()
    return event


def delete_event_participant(
    event: int,
    participant: int,
) -> Optional[Event]:
    event = Event.objects.filter(id=event).first()
    student = Student.objects.filter(id=participant).first()
    if event and student:
        event.participants.remove(student)
        event.save()
    return event


def get_event(event_id: int) -> Optional[Event]:
    return Event.objects.filter(id=event_id).first()

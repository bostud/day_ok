from typing import Generator
from ..models import (
    ClassRoom, Subject,
    Teacher, Student, Group, Service,
    Source,
)
from django import forms
from functools import partial

DateInput = partial(
    forms.DateInput,
    {'class': 'datepicker datepicker_now form-control'}
)

DateInputEmpty = partial(
    forms.DateInput,
    {'class': 'datepicker form-control'}
)

DateTimeInput = partial(
    forms.DateTimeInput,
    {'class': 'datepicker form-control'}
)


def get_classrooms() -> list:
    cl_r = ClassRoom.objects.all()
    res = []
    for room in cl_r:
        res.append((room.id, str(room)))
    return res


def get_subjects() -> list:
    iter_ = Subject.objects.all()
    res = []
    for i in iter_:
        res.append((i.id, str(i.name)))
    return res


def get_subjects_dummy() -> Generator:
    yield '', ''


def get_teachers() -> list:
    iter_ = Teacher.objects.filter(status=Teacher.Status.ACTIVE).all()
    res = []
    for i in iter_:
        if i.subjects:
            res.append((i.id, str(i)))
    return res


def get_students() -> list:
    iter_ = Student.objects.filter(status=Student.Status.ACTIVE).all()
    res = []
    for i in iter_:
        res.append((i.id, str(i)))
    return res


def get_groups() -> list:
    iter_ = Group.objects.all()
    res = []
    for i in iter_:
        if i.students:
            res.append((i.id, str(i)))
    return res


def get_services() -> Generator:
    res = Service.objects.all().values('id', 'name')
    for row in res:
        yield row['id'], row['name']


def get_sources() -> Generator:
    res = Source.objects.all().values('id', 'name')
    for r in res:
        yield r['id'], r['name']

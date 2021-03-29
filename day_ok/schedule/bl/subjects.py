from typing import Optional, List
from ..models import Subject
from datetime import timedelta


def add_subject(
    name: str,
    hour: int,
    minute: int,
) -> Optional[Subject]:
    duration = timedelta(hours=hour, minutes=minute)
    if s := Subject.objects.filter(name=name).first():
        return s
    s = Subject.objects.create(name=name, lessons_duration=duration)
    return s


def get_subjects(**kwargs) -> List[Optional[Subject]]:
    return Subject.objects.filter(status=Subject.Status.ACTIVE).all()


def get_subject(
    id_: int
) -> Optional[Subject]:
    return Subject.objects.filter(id=id_).first()


def delete_subject(
    id_: int,
) -> int:
    return Subject.objects.filter(id=id_).update(status=Subject.Status.DELETED)


def edit_subject(
    id_: int,
    name: str,
    hour: int,
    minute: int,
) -> Optional[Subject]:
    duration = timedelta(hours=hour, minutes=minute)
    Subject.objects.filter(id=id_).update(
        name=name,
        lessons_duration=duration,
    )
    return Subject.objects.filter(id=id_).first()

from typing import Optional, List
from ..models import Group
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class MyStudent:
    last_name: str
    first_name: str
    years_old: Optional[int]
    total_groups_services: int
    paid_groups_services: int
    group_lessons_paid: int
    group_lessons_present: int


@dataclass
class MyGroup:
    id: int
    name: str
    next_student: List[MyStudent]


def groups_objects():
    return Group.objects.all()


def get_group(id_: int) -> Optional[Group]:
    return Group.objects.filter(id=id_).first()


def get_group_info_by_period(
    group_id: int,
    dt_start: datetime,
    dt_end: datetime,
) -> Optional[MyGroup]:
    g = Group.objects.filter(id=group_id).first()
    dt_end = dt_end - timedelta(days=1)

    custom_group = MyGroup(next_student=[], name=g.name, id=g.id)
    for s in g.students.all():
        total_groups_services = s.get_total_groups_services(dt_start, dt_end)
        paid_groups_services = s.get_paid_groups_services(dt_start, dt_end)
        group_lessons_paid = s.get_group_lessons_paid(dt_start, dt_end)
        group_lessons_present = s.get_group_lessons_present(dt_start, dt_end)
        custom_group.next_student.append(
            MyStudent(
                first_name=s.first_name,
                last_name=s.last_name,
                years_old=s.years_old,
                total_groups_services=total_groups_services,
                paid_groups_services=paid_groups_services,
                group_lessons_paid=group_lessons_paid,
                group_lessons_present=group_lessons_present,
            )
        )
    return custom_group

from typing import Optional, List, Tuple
from ..models import Group, Student, Subject, Teacher, Lessons
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class MyStudent:
    id: int
    full_name: str
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
    return Group.objects.filter(status=Group.Status.ACTIVE).all()


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
        total_groups_services = s.get_total_groups_services(
            dt_start, dt_end, [g.subject])
        paid_groups_services = s.get_paid_groups_services(
            dt_start, dt_end, [g.subject])
        group_lessons_paid = s.get_group_lessons_paid(
            dt_start, dt_end, [g.subject])
        group_lessons_present = s.get_group_lessons_present(
            dt_start, dt_end, [g.subject])
        custom_group.next_student.append(
            MyStudent(
                id=s.id,
                full_name=s.full_name,
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


def add_group(
    name: str,
    age_from: str,
    students: List[int],
    subject: int,
    teacher: int,
) -> Tuple[Group, str]:
    if g := Group.objects.filter(name=name, status=Group.Status.ACTIVE).first():  # noqa
        return g, f'Group with name: {name} already exist'
    g = Group.objects.create(
        name=name,
        age_from=age_from,
        subject=Subject.objects.filter(id=subject).first(),
        teacher=Teacher.objects.filter(id=teacher).first(),
    )
    if students:
        g.students.add(
            *list(Student.objects.filter(id__in=[int(v) for v in students]).all())  # noqa
        )
        g.save()
    return g, ''


def edit_group(
    id_: int,
    name: str,
    age_from: str,
    students: List[int],
    subject: int,
    teacher: int,
) -> Tuple[Group, str]:
    if g := Group.objects.filter(name=name, status=Group.Status.ACTIVE).exclude(id=id_).first():  # noqa
        return g, f'Group with name: {name} already exist'
    if g := Group.objects.filter(id=id_).first():
        g.name = name
        g.age_from = age_from
        g.subject = Subject.objects.filter(id=subject).first()
        g.teacher = Teacher.objects.filter(id=teacher).first()

        if students:
            g.students.add(
                *list(Student.objects.filter(id__in=[int(v) for v in students]).all())  # noqa
            )
        g.save()
    return g, ''


def delete_group(
    id_: int,
) -> int:
    g = Group.objects.filter(id=id_).first()
    if g:
        if not Lessons.objects.filter(group=g).all():
            g.delete()
        else:
            Group.objects.filter(id=id_).update(status=Group.Status.DELETED)
        return 1
    return 0


def unpin_student(
    id_: int,
    student_id: int,
) -> Optional[Group]:
    if g := Group.objects.filter(id=id_).first():
        if s := Student.objects.filter(id=student_id).first():
            g.students.remove(s)
            g.save()
    return g

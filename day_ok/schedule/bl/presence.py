from typing import Optional, List
from ..models import Lessons, StudentPresence, Student


def all_presence(lessons_id: int) -> Optional[Lessons]:
    lessons = Lessons.objects.filter(id=lessons_id).first()
    if lessons:
        if lessons.lessons_type == Lessons.Type.INDIVIDUAL:
            students = [lessons.student] if lessons.student else []
        else:
            students = list(lessons.group.students.all())

        presence = StudentPresence.objects.filter(lessons=lessons).first()

        if not presence:
            presence = StudentPresence(lessons=lessons)
            presence.save()
        if not presence.is_all_present:
            presence.participants.add(*students)
            presence.save()

    return lessons


def get_all_presence(**kwargs) -> List[Optional[StudentPresence]]:
    query_filter = {}
    if groups := kwargs.get('groups'):
        query_filter['lessons__group__in'] = [int(v) for v in groups]
    if lessons_types := kwargs.get('lessons_types'):
        query_filter['lessons__lessons_type__in'] = [int(v) for v in lessons_types]  # noqa
    if students := kwargs.get('students'):
        query_filter['participants__in'] = [int(v) for v in students]
    if date_from := kwargs.get('date_from'):
        query_filter['lessons_date__gte'] = date_from
    if date_until := kwargs.get('date_until'):
        query_filter['lessons_date__lte'] = date_until

    query = StudentPresence.objects.filter(**query_filter)
    if page := kwargs.get('page'):
        per_page = kwargs.get('per_page')
        start = (int(page) - 1) * per_page
        end = start + per_page
        return query.all()[start:end]
    else:
        return query.all()


def get_lessons_presence(
    lessons: int
) -> StudentPresence:
    pr = StudentPresence.objects.filter(lessons__id=lessons).first()
    if not pr:
        lessons = Lessons.objects.filter(id=lessons).first()
        if lessons:
            pr = StudentPresence(lessons=lessons)
            pr.save()
    return pr


def edit_presence(
    lessons: int,
    students: List[int],
    clear_before_update: bool = False,
) -> StudentPresence:
    presence: StudentPresence = get_lessons_presence(lessons)
    if clear_before_update:
        presence.participants.clean()

    presence.participants.add(
        *list(Student.objects.filter(id__in=[int(s) for s in students]).all())
    )
    presence.save()

    return presence


def delete_student_presence(
    lessons: int,
    student: int,
) -> Optional[StudentPresence]:
    presence: Optional[StudentPresence] = (
        StudentPresence.objects.filter(lessons_id=lessons).first()
    )
    student = Student.objects.filter(id=student).first()
    if presence and student:
        presence.participants.remove(student)
        presence.save()
    return presence

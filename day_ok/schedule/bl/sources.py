from typing import List, Optional

from django.db.models import Count
from django.db import IntegrityError
from ..models import Student, Source
from ..data_classes.sources import SourceDataClass


def all_sources() -> list:
    return Source.objects.all()


def get_source_statistics() -> List[Optional[SourceDataClass]]:
    all_students = Student.objects.count()
    result = []
    max_percent = 0
    for res in Student.objects.values('source').annotate(count=Count('id')).order_by('count'):
        s = (
            Source.objects.filter(id=res['source']).first()
            if res['source'] else None
        )
        percent = round((res['count']/all_students) * 100, 2)
        if percent > max_percent:
            max_percent = percent
        result.append(SourceDataClass(
            name=s.name if s else '----',
            count=res['count'],
            percent=percent
        ))

    for res in result:
        res.percent_view = round(res.percent/max_percent * 100, 2)

    return result


def add_source(name: str) -> Source:
    try:
        s = Source(name=name)
        s.save()
    except IntegrityError:
        s = Source.objects.filter(name=name).first()

    return s


def delete_source(source_id: int) -> None:
    try:
        source_id = int(source_id)
        s = Source.objects.filter(id=source_id).first()
        if s:
            change_students_source(s)
            s.delete()
    except IntegrityError:
        pass


def change_students_source(
    old_source: Source,
    new_source: Optional[Source] = None,
) -> List[Optional[Student]]:
    for st in Student.objects.filter(source=old_source).all():
        st.source = new_source
        st.save()

    return Student.objects.filter(source=new_source).all()


def get_source(source_id: int) -> Optional[Source]:
    return Source.objects.filter(id=source_id).first()


def change_source_name(
    source_id: int,
    name: str,
) -> Optional[Source]:
    s = get_source(source_id)
    if s:
        s.name = name
        s.save()
    return s


def delete_student_source(
    student_id: int,
) -> Optional[Student]:
    st = Student.objects.filter(
        id=student_id,
    ).first()
    if st:
        st.source = None
        st.save()
    return st


def connect_student_to_source(
    students: List[int],
    source_id: int,
) -> List[Optional[Student]]:
    s = Source.objects.filter(id=int(source_id)).first()
    students = Student.objects.filter(id__in=students).all()
    if s and students:
        for st in students:
            st.source = s
            st.save()
    return students

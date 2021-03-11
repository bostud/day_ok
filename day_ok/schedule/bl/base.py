from typing import List, Optional

from django.db.models import Count
from ..models import Student, Source
from ..data_classes.base import SourceDataClass


def get_source_statistics() -> List[Optional[SourceDataClass]]:
    all_students = Student.objects.count()

    for res in Student.objects.values('source').annotate(count=Count('id')):
        s = (
            Source.objects.filter(id=res['source']).first()
            if res['source'] else None
        )
        yield SourceDataClass(
            name=s.name if s else '----',
            count=res['count'],
            percent=round(res['count']/all_students, 2) * 100
        )

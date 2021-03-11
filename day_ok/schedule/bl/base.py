from typing import List, Optional

from django.db.models import Count
from ..models import Student, Source
from ..data_classes.base import SourceDataClass


def get_source_statistics() -> List[Optional[SourceDataClass]]:
    all_students = Student.objects.count()
    result = []
    max_percent = 0
    for res in Student.objects.values('source').annotate(count=Count('id')):
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


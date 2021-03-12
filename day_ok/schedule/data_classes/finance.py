from typing import List
from dataclasses import dataclass
from ..models import Teacher, Subject, Lessons


@dataclass
class TeacherSubjectStat:
    subject: Subject

    individual_lessons: List[Lessons]
    group_lessons: List[Lessons]

    @property
    def individual_count(self):
        return len(self.individual_lessons)

    @property
    def group_count(self):
        return len(self.group_lessons)

    @property
    def total_lessons_count(self) -> int:
        return self.individual_count + self.group_count


@dataclass
class TeacherMonthStat:
    teacher: Teacher

    subjects_stat: List[TeacherSubjectStat]

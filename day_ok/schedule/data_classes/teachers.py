from typing import List
from dataclasses import dataclass
from ..models import Lessons, Subject


@dataclass
class SubjectReport:
    subject: Subject
    count: int
    lessons: List[Lessons]


@dataclass
class LessonsReport:
    lessons_type_name: str
    lessons_type_id: int
    count: int
    subjects_reports: List[SubjectReport]

    @property
    def is_individual(self):
        return int(self.lessons_type_id) == Lessons.Type.INDIVIDUAL

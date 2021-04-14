import datetime
from typing import List
from dataclasses import dataclass
from ..models import Lessons, Subject
from ..utils import datetime_now_tz


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


@dataclass
class DailyLessonsReport:
    lessons: List[Lessons]
    date: datetime.date
    show_lessons: bool = True

    @property
    def style(self):
        return 'grey' if not self.show_lessons else 'white'

    @property
    def is_today(self):
        return self.date == datetime_now_tz().date()


@dataclass
class WeeklyLessonsReport:
    week_number: int
    date_from: datetime.date
    date_to: datetime.date
    report: List[DailyLessonsReport]

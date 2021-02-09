from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


# Create your models here.
INDIVIDUAL = '1'
GROUP = '2'
CLASS_ROOM_TYPES = [
    (INDIVIDUAL, _('індивідуальний')),
    (GROUP, _('груповий'))
]

LESSONS_TYPES = [
    (INDIVIDUAL, _('індивідуальне')),
    (GROUP, _('групове'))
]

INVOICE_STATUSES = [
    ('1', _('оплачено')),
    ('2', _('очікуємо оплати')),
    ('3', _('закрито')),
    ('4', _('тестове заняття')),
]


class Subject(models.Model):
    name = models.CharField(max_length=100)
    lessons_duration = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.name


class ContactMixin(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    phone_number = models.CharField(max_length=13, blank=False)  # +380995588779
    email = models.CharField(max_length=150, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(ContactMixin):
    date_release = models.DateTimeField(blank=True, null=True)
    subject = models.ManyToManyField(Subject)


class Student(ContactMixin):
    date_test_lessons = models.DateTimeField(default=now)
    date_start_studying = models.DateTimeField(blank=True, null=True)
    parent_phone = models.CharField(max_length=13, blank=True, null=True)
    parent_first_name = models.CharField(max_length=50, blank=True, null=True)
    parent_last_name = models.CharField(max_length=100, blank=True, null=True)


class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    places_count = models.IntegerField(blank=True, null=True, default=None)
    room_type = models.CharField(
        max_length=2,
        choices=CLASS_ROOM_TYPES,
        default=GROUP,
    )
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Аудиторія: {self.name}, " \
               f"Тип: {self.get_room_type_name(str(self.room_type))}"

    @staticmethod
    def get_room_type_name(room_type: str):
        for k, v in CLASS_ROOM_TYPES:
            if k == room_type:
                return v


class Group(models.Model):
    name = models.CharField(max_length=150)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    age_from = models.IntegerField(default=0)

    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.name}, Вік: {self.age_from}+, {self.subject.name}"


class Lessons(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.DO_NOTHING)
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    lessons_type = models.CharField(max_length=2, choices=LESSONS_TYPES)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)

    students = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.class_room}, {self.date}, {self.lessons_type}"


class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    lessons_count = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=3, default='UAH')

    def __str__(self):
        return self.name


class Invoice(models.Model):
    number = models.CharField(unique=True, db_index=True, max_length=100)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(
        Teacher,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    date_created = models.DateTimeField(auto_now=True)
    date_when_should_pay = models.DateField()
    status = models.CharField(max_length=2, choices=INVOICE_STATUSES)

    def __str__(self):
        return f"{self.number}, Статус: {self.status}, Учень: {self.student}"

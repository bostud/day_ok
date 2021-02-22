import json
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

STATUS_TEACHER_ACTIVE = '1'
STATUS_TEACHER_VACATION = '2'
STATUS_TEACHER_INACTIVE = '3'
TEACHER_STATUSES = [
    (STATUS_TEACHER_ACTIVE, _('активний')),
    (STATUS_TEACHER_VACATION, _('відпустка')),
    (STATUS_TEACHER_INACTIVE, _('неактивний')),
]


STATUS_STUDENT_ACTIVE = '1'
STATUS_STUDENT_INACTIVE = '2'
STUDENT_STATUSES = [
    (STATUS_STUDENT_ACTIVE, _('активний')),
    (STATUS_STUDENT_INACTIVE, _('неактивний')),
]

INVOICE_RECEIVERS = [
    ('1', 'Школа'),
    ('2', 'Вчитель'),
]


class Subject(models.Model):
    class Meta:
        verbose_name = 'Предмети'
        verbose_name_plural = 'Предмети'

    name = models.CharField(
        'Назва предмету',
        max_length=100
    )
    lessons_duration = models.DurationField(
        'Тривалість заняття',
    )

    def __str__(self):
        return self.name


class ContactMixin(models.Model):
    first_name = models.CharField(
        'Імʼя',
        max_length=50, 
        blank=False
    )
    last_name = models.CharField(
        'Прізвище', max_length=100, blank=False)
    phone_number = models.CharField(
        'Номер телефону', max_length=13, blank=False)  # +380995588779
    email = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField('Дата народження', blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Teacher(ContactMixin):
    class Meta:
        verbose_name = 'Викладачі'
        verbose_name_plural = 'Викладачі'

    status = models.CharField(
        'Статус',
        max_length=2,
        choices=TEACHER_STATUSES,
        default=TEACHER_STATUSES[0][0],
    )
    date_release = models.DateTimeField(
        'Дата звільнення', blank=True, null=True)
    subjects = models.ManyToManyField(
        Subject, verbose_name='Предмети', blank=True)


class Source(models.Model):
    class Meta:
        verbose_name = 'Джерела'
        verbose_name_plural = 'Джерела'

    name = models.CharField('Назва', max_length=100)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def students_from_source_total(self):
        q = (
            Student.objects.filter(source=self)
        )
        return q.count()

    students_from_source_total.short_description = 'К-сть учнів'


class Student(ContactMixin):
    class Meta:
        verbose_name = 'Учні'
        verbose_name_plural = 'Учні'

    source = models.ForeignKey(
        Source,
        on_delete=models.DO_NOTHING,
        verbose_name='Звідки дізнались про нашу школу?',
        blank=True,
        null=True,
    )
    status = models.CharField(
        'Статус',
        max_length=2,
        choices=STUDENT_STATUSES,
        default=STUDENT_STATUSES[0][0],
    )
    date_test_lessons = models.DateTimeField(
        'Дата тестового заняття', default=now)
    date_start_studying = models.DateTimeField(
        'Дата старту навчання', blank=True, null=True)
    date_end_studying = models.DateTimeField(
        'Дата закінчення навчання', blank=True, null=True)
    parent_phone = models.CharField(
        'Номер телефону батьків', max_length=13, blank=True, null=True)
    parent_first_name = models.CharField(
        'Імʼя одного з батьків', max_length=50, blank=True, null=True)
    parent_last_name = models.CharField(
        'Прізвище одного з батьків', max_length=100, blank=True, null=True)


class ClassRoom(models.Model):
    class Meta:
        verbose_name = 'Аудиторії'
        verbose_name_plural = 'Аудиторії'

    name = models.CharField('Назва аудиторії', max_length=100)
    places_count = models.IntegerField(
        'К-сть місць', blank=True, null=True, default=None)
    room_type = models.CharField(
        'Тип аудиторії',
        max_length=2,
        choices=CLASS_ROOM_TYPES,
        default=GROUP,
    )
    description = models.TextField('Додатково', max_length=500, blank=True)

    def __str__(self):
        return f"Аудиторія: {self.name}, " \
               f"Тип: {self.get_room_type_name}"

    @property
    def get_room_type_name(self):
        for k, v in CLASS_ROOM_TYPES:
            if self.room_type == k:
                return v


class Group(models.Model):
    class Meta:
        verbose_name = 'Групи'
        verbose_name_plural = 'Групи'

    name = models.CharField('Назва групи', max_length=150)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.DO_NOTHING,
        verbose_name='Предмет',
        blank=True,
        null=True,
    )
    age_from = models.IntegerField('Вік з', default=0)

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.DO_NOTHING,
        verbose_name='Викладач',
        blank=True,
        null=True,
    )
    students = models.ManyToManyField(
        Student, verbose_name='Учні', blank=True)

    def __str__(self):
        return f"{self.name}, Вік: {self.age_from}+"

    def students_count(self):
        return self.students.count()

    students_count.short_description = 'К-сть учнів'


class LessonsParent(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    date_from_valid = models.DateField(null=True, blank=True)
    date_until_valid = models.DateField(blank=True, null=True)
    weekdays_for_repeating = models.JSONField(
        blank=True, editable=True, null=True)

    @property
    def weekdays_list(self):
        if self.weekdays_for_repeating:
            return [
                int(v)
                for v in json.loads(str(self.weekdays_for_repeating))
            ]
        else:
            return ''

    @property
    def count_of_children(self):
        return Lessons.objects.filter(parent=self).count()


class Lessons(models.Model):
    class Meta:
        verbose_name = 'Заняття'
        verbose_name_plural = 'Заняття'

    class_room = models.ForeignKey(
        ClassRoom, on_delete=models.DO_NOTHING, verbose_name='Аудиторія')
    date = models.DateField('Дата заняття')
    time_start = models.TimeField('Час початку')
    time_end = models.TimeField('Час закінчення')
    lessons_type = models.CharField(
        'Тип заняття', max_length=2, choices=LESSONS_TYPES)
    subject = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, verbose_name='Предмет')
    teacher = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING, verbose_name='Викладач')

    student = models.ForeignKey(
        Student,
        on_delete=models.DO_NOTHING,
        verbose_name='Учень',
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.DO_NOTHING,
        verbose_name='Група',
        blank=True,
        null=True,
    )

    parent = models.ForeignKey(
        LessonsParent,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name='Творець'
    )

    def __str__(self):
        return f"{self.class_room.name}/{self.get_lessons_type_name}"

    def format_date(self):
        return self.date.strftime('%d.%m.%Y')

    def format_time_start(self):
        return self.time_start.strftime("%H:%M")

    def format_time_end(self):
        return self.time_end.strftime("%H:%M")

    def duration(self):
        end_minutes = self.time_end.hour * 60 + self.time_end.minute
        start_minute = self.time_start.hour * 60 + self.time_start.minute

        return (end_minutes - start_minute) / 60

    @property
    def get_lessons_type_name(self):
        for _id, name in LESSONS_TYPES:
            if self.lessons_type == _id:
                return name
        return '(undefined)'

    format_date.short_description = 'Дата заняття'
    format_time_start.short_description = 'Час початку'
    format_time_end.short_description = 'Час закінчення'
    duration.short_description = 'Тривалість, год.'

    @property
    def format_t_start(self):
        return self.format_time_start()

    @property
    def format_t_end(self):
        return self.format_time_end()

    @property
    def condition_individual(self):
        return self.lessons_type == INDIVIDUAL

    @property
    def presence_count(self):
        return StudentPresence.objects.filter(lessons=self).count()

    @property
    def students_count(self):
        if self.condition_individual:
            return 1
        else:
            return self.group.students.count()


class Service(models.Model):
    class Meta:
        verbose_name = 'Послуги'
        verbose_name_plural = 'Послуги'

    name = models.CharField('Назва послуги', max_length=50)
    price = models.IntegerField('Ціна',)
    lessons_count = models.IntegerField('К-сть занять', blank=True, null=True)
    currency = models.CharField('Валюта', max_length=3, default='UAH')

    def __str__(self):
        return self.name


def get_new_unique_invoice_number():
    last = Invoice.objects.last()
    if not last:
        last_id = 0
    else:
        last_id = last.id

    return f'INVOICE-{last_id + 1}-{now().strftime("%d%m%Y")}'


class Invoice(models.Model):
    class Meta:
        verbose_name = 'Рахунки'
        verbose_name_plural = 'Рахунки'

    number = models.CharField(
        'Унікальний номер рахунку',
        unique=True,
        db_index=True,
        max_length=100,
        default=get_new_unique_invoice_number,
    )
    student = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, verbose_name='Студент')
    service = models.ForeignKey(
        Service, on_delete=models.DO_NOTHING, verbose_name='Послуга')
    receiver = models.CharField(
        'Отримувач',
        max_length=2,
        choices=INVOICE_RECEIVERS,
        default=INVOICE_RECEIVERS[0][0],
    )
    receiver_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name='Вчитель',
    )
    date_created = models.DateTimeField(auto_now=True)
    date_when_should_pay = models.DateField('Дата до якої здійснити оплату')
    status = models.CharField(
        'Статус рахунку', max_length=2, choices=INVOICE_STATUSES)

    def __str__(self):
        return f'{self.number}'


class StudentPresence(models.Model):
    class Meta:
        verbose_name = 'Відвідування'
        verbose_name_plural = 'Відвідування'
        unique_together = [
            ['lessons', 'student'],
        ]

    lessons = models.ForeignKey(
        Lessons, on_delete=models.CASCADE,
        verbose_name='Заняття',
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Учень',
    )
    is_presence = models.BooleanField(
        default=True,
        verbose_name='Був присутній?',
    )
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lessons}/{self.student}"


class Event(models.Model):
    class Meta:
        verbose_name = 'Заходи'
        verbose_name_plural = 'Заходи'
    name = models.CharField(
        verbose_name='Назва заходу',
        max_length=150,
    )
    date_created = models.DateTimeField(auto_now=True)
    date_of_event = models.DateField(
        verbose_name='Дата заходу',
        default=now,
    )
    time_start = models.TimeField(
        verbose_name='Час початку(не обовʼязково)',
        blank=True,
        null=True,
        default=None,
    )
    time_end = models.TimeField(
        verbose_name='Час закінчення(не обовʼязково)',
        blank=True,
        null=True,
        default=None,
    )
    class_room = models.ForeignKey(
        ClassRoom,
        on_delete=models.DO_NOTHING,
        verbose_name='Аудиторія'
    )
    participants = models.ManyToManyField(
        Student,
        verbose_name='Учасники'
    )

    def __str__(self):
        return str(self.name)

    @property
    def participants_count(self):
        return self.participants.count()

    @property
    def format_t_start(self):
        return self.format_time_start()

    @property
    def format_t_end(self):
        return self.format_time_end()

    def format_date(self):
        return self.date_of_event.strftime('%d.%m.%Y')

    def format_time_start(self):
        if self.time_start:
            return self.time_start.strftime("%H:%M")
        return '--:--'

    def format_time_end(self):
        if self.time_end:
            return self.time_end.strftime("%H:%M")
        return '--:--'

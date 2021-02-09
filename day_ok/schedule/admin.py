from django.contrib import admin

# Register your models here.
from .models import (
    ClassRoom, Service, Teacher, Group, Student, Subject, Invoice, Lessons,
)

admin.site.register(ClassRoom)
admin.site.register(Service)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Invoice)
admin.site.register(Lessons)

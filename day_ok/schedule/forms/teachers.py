from django import forms


class TeacherLessonsColorForm(forms.Form):
    color = forms.CharField(max_length=10)

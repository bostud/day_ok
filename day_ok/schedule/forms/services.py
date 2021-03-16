from django import forms


class GetServiceSubjectsForm(forms.Form):
    service = forms.IntegerField()

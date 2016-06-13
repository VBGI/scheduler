# coding: utf-8

from django.forms import ModelForm
from .models import ScheduleModel


class UserFillForm(ModelForm):
    class Meta:
        model = ScheduleModel
        fields = ('username', 'phone', 'email', 'num')

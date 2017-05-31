# coding: utf-8

from .models import ScheduleModel
from django import forms


class UserFillForm(forms.ModelForm):
    def __init__(self, thenum, *args, **kwargs):
        super(UserFillForm, self).__init__(*args, **kwargs)
        self.fields['num'] = forms.ChoiceField(choices=[ (i+1, i+1) for i in range(min(5,thenum))],
                                               label=u"Количество детей")
    
    class Meta:
        model = ScheduleModel
        fields = ('username', 'phone', 'email', 'num')

# -*- coding: utf-8 -*-

from django import template

from ..forms import UserFillForm
from ..models import ScheduleDates, ScheduleName

register = template.Library()


@register.inclusion_tag('scheduler_regform.html')
def show_form(pk):
    error = ''
    try:
        dates = ScheduleDates.objects.filter(name=pk)
    except ScheduleDates.DoesNotExist:
        error = u'Не определено ни одного расписания'
    return {'error': error,
            'dates': dates,
            'userform': UserFillForm(),
            'schedule_pk': pk
            }


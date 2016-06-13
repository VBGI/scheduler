# -*- coding: utf-8 -*-

from django import template

from ..forms import UserFillForm
from ..models import ScheduleDates

register = template.Library()


@register.inclusion_tag('scheduler_regform.html')
def show_form(name):
    error = ''
    try:
        dates = ScheduleDates.objects.filter(name__name__iexact='name')
    except ScheduleDates.DoesNotExist:
        error = 'Не определено ни одного расписания'
    return {'error': error,
            'dates': dates,
            'userform': UserFillForm(),
            'schedule_hash': hex(hash(name))[3:]
            }

# @register.filter_function
# def order_by(queryset, args):
#     args = [x.strip() for x in args.split(',')]
#     return queryset.order_by(*args)
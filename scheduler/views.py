# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csfr_exempt
from django.contrib.auth import get_user_model
from .models import ScheduleModel, ScheduleTimes

import re
# def _from_iso(dstr, dtype='datetime'):
#     if dstr is None: return None
#     if dtype == 'datetime':
#         return datetime.datetime(*map(int, re.split('[^\d]', dstr)))
#     if dtype == 'date':
#         return datetime.date(*map(int, re.split('[^\d]', dstr)))
#     if dtype == 'time':
#         return datetime.time(*map(int, re.split('[^\d]', dstr)))

def validate(uname, phone):
    err_msg = ''
    if not re.match(r'^[\-\+\d]+$', phone):
        err_msg = 'Неправильный формат тел. номера'
    if not uname:
        err_msg = 'Имя не задано'
    return err_msg

@never_cache
@csrf_exempt
def register_user(request):
    response_data = {'error' : '', 'msg': '', 'ferr': ''}
    if request.method == 'POST':
        timepk = request.POST.get('timepk', None)
        uname = request.POST.get('username', '')
        uphone = request.POST.get('phone', '')
        umail = request.POST.get('email', '')
        unum = request.POST.get('num', '')
        upk = request.POST.get('upk', '')
        try:
            user = get_user_model().objects.get(pk=upk)
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Внутренняя ошибка при определении принадлежности к расписанию'}))

        err_msg = validate(uname, uphone)
        if not err_msg:
            try:
                timeobj = ScheduleTimes.objects.get(id=timepk)
            except ScheduleTimes.DoesNotExist:
                response_data.update({'error': 'Неправильно выбрано время'})
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            if timeobj.get_free_places <= 0:
                response_data.update({'error': 'Выбранное время занято'})
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            try:
                unum = int(unum)
                umod = ScheduleModel.objects.create(username=uname,
                                                    phone=uphone,
                                                    email=umail,
                                                    num=unum,
                                                    time=timeobj,
                                                    user=user)
                response_data.update({'msg': 'Вы успешно зарегистрировались'})
            except:
                response_data.update({'error': 'Что-то пошло не так при регистрации'})
        else:
            response_data.update({'error':err_msg})
    else:
        response_data['error'] = 'Неправильный запрос'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

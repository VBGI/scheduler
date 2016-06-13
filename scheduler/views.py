# import datetime
import json
# import re

from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import UserFillForm
from .models import ScheduleModel, ScheduleTimes


# def _from_iso(dstr, dtype='datetime'):
#     if dstr is None: return None
#     if dtype == 'datetime':
#         return datetime.datetime(*map(int, re.split('[^\d]', dstr)))
#     if dtype == 'date':
#         return datetime.date(*map(int, re.split('[^\d]', dstr)))
#     if dtype == 'time':
#         return datetime.time(*map(int, re.split('[^\d]', dstr)))

@csrf_protect
@never_cache
def register_user(request):
    response_data = {'error' : '', 'msg': '', 'ferr': ''}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserFillForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            timepk = request.POST.get('timepk', None)
            try:
                timeobj = ScheduleTimes.objects.get(id=timepk)
            except SceduleTimes.DoesNotExist:
                response_data.update({'error': 'Неправильно выбрано время'})
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            uname = form.cleaned_data['username']
            uphone = form.cleaned_data['phone']
            umail = form.cleaned_data['email']
            unum = form.cleaned_data['num']
            try:
                umod = ScheduleModel.objects.create(username=uname,
                                                    phone=uphone,
                                                    email=umail,
                                                    num=unum,
                                                    time=timeobj)
                response_data.update({'msg', 'Вы успешно зарегистрировались на мероприятие'})
            except:
                response_data.update({'error': 'Что-то пошло не так при регистрации'})
        else:
            response_data.update({'error': 'Неправильно заполнены поля формы', 'ferr': form.errors})
    else:
        response_data['error'] = 'Неправильный запрос'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

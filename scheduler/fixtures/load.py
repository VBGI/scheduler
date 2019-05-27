from __future__ import print_function

import sys, os

from datetime import date, time

sys.path.append('/home/scidam/webapps/bgicms242/bgi')
os.environ['DJANGO_SETTINGS_MODULE']='bgi.settings'

from .datareg import data
from ..models import ScheduleName, ScheduleDates, ScheduleTimes

from django.contrib.auth import get_user_model



CDIR = os.path.dirname(os.path.abspath(__file__))


usermodel = get_user_model()


send_template = """
Здравствуйте, {}!

Для вас была создана регистрационная форма 
в рамках проекта "Наука в Путешествии".

Данные для авторизации:
=======================

Путь для авторизации: http://botsad.ru/admin-reg/
Имя пользователя: {}
Пароль: {}

Вы можете сменить пароль после авторизации.

Перечень зарегистрированных участников
доступен по ссылке (необходима авторизация): http://botsad.ru/admin-reg/

Регистрационная форма также доступна на сайте БСИ ДВО РАН по ссылке: http://botsad.ru/reg/{}

Код для интеграции формы на Ваш сайт:

<!-- Начало кода {} -->
<iframe src="http://botsad.ru/reg/{}" width="600" height="300" align="center">Ваш браузер не поддерживает плавающие фреймы!</iframe>
<!-- Конец кода {} -->



Это письмо сегенрировано автоматически. Отвечать на него не нужно.

""".format()

theme_template = "Регистрационная форма (Наука в Путешествии)"


# -------- utility function
import re
timepat = re.compile('\d\d:\d\d')


def parse_times(s):
    pats = timepat.findall('s')
    times = [(int(item.split(':')[0]), int(item.split(':')[1])) for item in pats]
    result = [time(hour=t[0], minute=t[1]) for t in times]
    return result
    
    



# --------------- Loading & processing the data ---------

for item in data:
    # -------------- evaluating data item, sending mail after completion....
    if item['dateonly']:
        maxnum = 2000
    else:
        maxnum = 5
    
    um, _ = usermodel.objects.get_or_create(username=item['username'], active=True)
    
    schm, _ = ScheduleName.objects.get_or_create(name=item['name'], user=um, maxnumber=maxnum)
    
    for d in item['dates']:
        mo = int(d['month'])
        for day in d['days']:
            schd,_ = ScheduleDates.objects.get_or_create(name=schm, user=um, date=date(year=2019, month=mo, day=day), dateonly=item['dateonly'])
        if item['dateonly']:
            ScheduleTimes.objects.get_or_create(date=schd, user=um, time=time(hour=11, minute=0, second=0))
        else:
            for t in parse_times(item['times']):
                ScheduleTimes.objects.get_or_create(date=schd, user=um, time=t)
    
    # --------------------
    
    
    
    # -------- sending email

    

# -------------------------------------------------------

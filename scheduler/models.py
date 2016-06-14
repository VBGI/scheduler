#coding: utf-8

import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from cms.models.pluginmodel import CMSPlugin

class ScheduleName(models.Model):
    name = models.CharField(max_length=20, blank=False,
                            verbose_name="Название", default="Без имени")
    mininterval = models.IntegerField(default=60, verbose_name=_("Интервал, мин."))
    starttime = models.TimeField(default=datetime.time(hour=11), verbose_name=_("Начало"))
    endtime = models.TimeField(default=datetime.time(hour=11), verbose_name=_("Конец"))
    maxnumber = models.IntegerField(default=3, verbose_name=_("Число участников max."))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Наименование расписания')
        verbose_name_plural = _('Наименования расписаний')


class ScheduleDates(models.Model):
    name = models.ForeignKey(ScheduleName, verbose_name="Расписание", related_name='dates')
    date = models.DateField(default=timezone.now())

    def __unicode__(self):
        return self.name.name + '|' + str(self.date)

    class Meta:
        verbose_name = _('Дата события')
        verbose_name_plural = _('Даты событий')
        ordering = ('date',)


class ScheduleModel(models.Model):
    THENUM = ((1, 'Один'), (2, 'Два'), (3, 'Три'))
    username = models.CharField(max_length=100, default='', blank=True, verbose_name=_("Имя"))    
    phone = models.CharField(max_length=20, default='', blank=True, verbose_name=_("Телефон"))
    email = models.EmailField(blank=True)
    num = models.IntegerField(default=1, choices=THENUM, verbose_name=_("Число участников"), blank=True)
    time = models.ForeignKey('ScheduleTimes', null=True, related_name='registered', verbose_name=_("Время"))

    def __unicode__(self):
        return self.username + '|' + self.phone + '|' + str(self.time.date.date) + '|' + str(self.time.time)

    class Meta:
        verbose_name = _('Запись регистрации')
        verbose_name_plural = _('Записи регистрации')


class ScheduleTimes(models.Model):
    date = models.ForeignKey(ScheduleDates, verbose_name="Дата", related_name='times')
    time = models.TimeField(default=timezone.now())

    def __unicode__(self):
        return self.date.name.name + '|' + str(self.date.date) + '|' + str(self.time)

    class Meta:
        verbose_name = _('Время регистрации')
        verbose_name_plural = _('Времена регистрации')
        ordering = ('time',)

    @property
    def get_registered(self):
        return self.registered.aggregate(models.Sum('num'))['num__sum'] or 0

    @property
    def get_free_places(self):
        return self.date.name.maxnumber - self.get_registered 



class SchedulePlugin(CMSPlugin):
    schedule = models.ForeignKey(ScheduleName, verbose_name=u"Название расписания")
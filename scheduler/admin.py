#coding: utf-8
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext as _
import datetime

from .models import ScheduleName, ScheduleDates, ScheduleModel, ScheduleTimes


class ScheduleTimesInline(admin.TabularInline):
    model = ScheduleTimes
    fieldsets = ((None, {'fields': ['time', 'get_registered', 'get_free_places']}),)
    readonly_fields=('get_registered', 'get_free_places')
    extra = 1

class ScheduleDatesAdmin(admin.ModelAdmin):
    inlines = [ScheduleTimesInline]

class ScheduleModelAdmin(admin.ModelAdmin):
    list_display = ('get_date', 'get_time','username', 'phone', 'num', 'email')
    list_filter = ('time__date__date',)
    def get_time(self, obj):
        return obj.time.time.strftime('%H:%M')
    get_time.admin_order_field  = 'time'
    get_time.short_description=_("Время")

    def get_date(self, obj):
        return obj.time.date.date.strftime('%a, %d %b %Y')
    get_date.admin_order_field  = 'time'
    get_date.short_description=_("Дата")


class ScheduleNameAdmin(admin.ModelAdmin):
    actions = ['create_schedule']

    def create_schedule(self, request, queryset):
        thenum = 0
        for item in queryset:
            for date in item.dates.all():
                ctime = item.starttime
                while ctime < item.endtime:
                    ctime = (datetime.datetime.combine(datetime.date(1,1,1), ctime) + datetime.timedelta(minutes=item.mininterval)).time()
                    ss = ScheduleTimes(date=date, time=ctime)
                    ss.save()
                    thenum += 1
        self.message_user(request, u"Было создано %s записи" % thenum)
    create_schedule.short_description = u'Генерировать расписание' 
    
    
admin.site.register(ScheduleModel, ScheduleModelAdmin)

admin.site.register(ScheduleDates, ScheduleDatesAdmin)

admin.site.register(ScheduleName, ScheduleNameAdmin)
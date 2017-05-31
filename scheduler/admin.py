# coding: utf-8

from django.contrib import admin
from django.utils.translation import gettext as _
import datetime
from django.contrib.admin import SimpleListFilter
from django.contrib.auth import get_user_model
from .models import ScheduleName, ScheduleDates, ScheduleModel, ScheduleTimes


class PermissionMixin:

    def queryset(self, request):
        if request.user.has_perm('scheduler.can_edit_all'):
            return self.model.objects.all()
        else:
            return self.model.objects.filter(user=request.user)

    def _common_permission_manager(self, request, obj):
        cperm = request.user.has_perm('scheduler.can_edit_all')
        if cperm:
            return True
        if obj:
            if request.user != obj.user:
                return False
            else:
                return True
        return True

    def has_delete_permission(self, request, obj=None):
        return self._common_permission_manager(request, obj)

    def has_change_permission(self, request, obj=None):
        return self._common_permission_manager(request, obj)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()

#    def get_readonly_fields(self, request, obj=None):
#        readonly_fields = []
#        if not request.user.is_superuser:
#            readonly_fields.append('user')
#        return readonly_fields


class SchedulerCustomListFilter(SimpleListFilter):
    title = _('Пользователь')
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        res = []
        umodel = get_user_model()
        for item in list(set(map(lambda x: x.user.username, ScheduleName.objects.all().exclude(user__isnull=True)))):
            try:
                uinstance = umodel.objects.get(username__iexact=item)
                res.append((uinstance.id, uinstance.username))
            except umodel.DoesNotExist:
                pass
        return tuple(res)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__id__exact=self.value())
        else:
            return queryset


class ScheduleTimesInline(PermissionMixin, admin.TabularInline):
    model = ScheduleTimes
    readonly_fields = ['get_registered', 'get_free_places']
    fieldsets = ((None, {'fields': ['time', 'get_registered', 'get_free_places']}),)
    extra = 0


class ScheduleDatesAdmin(PermissionMixin, admin.ModelAdmin):
    inlines = [ScheduleTimesInline]

    def get_list_filter(self, request):
        list_filter = super(ScheduleDatesAdmin, self).get_list_filter(request)
        if request.user.has_perm('scheduler.can_edit_all'):
            list_filter += (SchedulerCustomListFilter, )
        return list_filter

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if not request.user.has_perm('scheduler.can_edit_all'):
            readonly_fields.append('user')
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super(ScheduleDatesAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.has_perm('scheduler.can_edit_all'):
            form.base_fields['name'].queryset = form.base_fields['name'].queryset.filter(user=request.user)
        return form


class ScheduleModelAdmin(PermissionMixin, admin.ModelAdmin):
    list_display = ('get_date', 'get_time', 'username', 'phone', 'num', 'email')
    list_filter = ('time__date__date',)

    def get_time(self, obj):
        return obj.time.time.strftime('%H:%M')
    get_time.admin_order_field = 'time'
    get_time.short_description = _("Время")

    def get_date(self, obj):
        return obj.time.date.date.strftime('%a, %d %b %Y')
    get_date.admin_order_field = 'time__date__date'
    get_date.short_description = _("Дата")

    def get_list_filter(self, request):
        list_filter = super(ScheduleModelAdmin, self).get_list_filter(request)
        if request.user.has_perm('scheduler.can_edit_all'):
            list_filter += (SchedulerCustomListFilter,)
        return list_filter

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if not request.user.has_perm('scheduler.can_edit_all'):
            readonly_fields.append('user')
        return readonly_fields


class ScheduleNameAdmin(PermissionMixin, admin.ModelAdmin):
    actions = ['create_schedule']

    def create_schedule(self, request, queryset):
        thenum = 0
        for item in queryset:
            for date in item.dates.all():
                ctime = item.starttime
                while ctime < item.endtime:
                    ctime = (datetime.datetime.combine(datetime.date(1, 1, 1), ctime) + datetime.timedelta(minutes=item.mininterval)).time()
                    ScheduleTimes.objects.get_or_create(date=date, time=ctime, user=request.user)
                    thenum += 1
        self.message_user(request, u"Было создано %s записи" % thenum)
    create_schedule.short_description = u'Генерировать расписание'

    def get_list_filter(self, request):
        list_filter = super(ScheduleNameAdmin, self).get_list_filter(request)
        if request.user.has_perm('scheduler.can_edit_all'):
            list_filter += (SchedulerCustomListFilter,)
        return list_filter

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if not request.user.has_perm('scheduler.can_edit_all'):
            readonly_fields.append('user')
        return readonly_fields


admin.site.register(ScheduleModel, ScheduleModelAdmin)
admin.site.register(ScheduleDates, ScheduleDatesAdmin)
admin.site.register(ScheduleName, ScheduleNameAdmin)

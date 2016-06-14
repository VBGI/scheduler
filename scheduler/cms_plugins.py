# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import SchedulePlugin


class SheduleMainPlugin(CMSPluginBase):
    model = SchedulePlugin
    name = u"Отображение расписания"
    render_template = "scheduler_plugin.html"
    text_enabled = False
    def render(self, context, instance, placeholder):
        context.update({'object': instance})
        return context

plugin_pool.register_plugin(SheduleMainPlugin)
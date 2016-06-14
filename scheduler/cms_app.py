# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class SchedulerApphook(CMSApp):
    name = _(u"Ajax-служба приложения регистрации")
    urls = ["scheduler.urls"]

apphook_pool.register(SchedulerApphook)
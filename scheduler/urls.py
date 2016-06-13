# -*- coding: utf-8 -*-

from django.conf.urls import *

urlpatterns = patterns('',
   url(r'^scheduler/$', 'scheduler.views.register_user')
)
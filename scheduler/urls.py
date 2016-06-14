# -*- coding: utf-8 -*-

from django.conf.urls import *
from .views import register_user

urlpatterns = patterns('',
   url(r'^scheduler/$', register_user, name="bgi-scheduler")
)
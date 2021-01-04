# coding=utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add/$', views.add),
    url(r'^edit/$', views.edit),
    url(r'^delete/$', views.delete),
    url(r'^subscribe/$', views.subscribe),
    #todo  订阅界面订阅类别、资源类别、资源路径字典码映射
    #todo  订阅页面发起订阅、取消订阅
]
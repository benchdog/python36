#coding: utf8
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01 import models

# Create your views here.

# def index(request):
#     # return HttpResponse(sys.path)
#     system_list = models.t_viid_system.objects.all()
#     return HttpResponse(system_list.query)

# def ape_stat(request):
#     if request.method == 'GET':#GET区分大小写
#         return render(request,'ape_stat.html')
#         # return HttpResponse(BASE_DIR)

def index(request):
    viids = models.t_viid_system.objects.all()
    for i in viids:
        i.onlineStatus = '在线' if i.onlineStatus == 1 else '离线'
        i.type = '上级' if i.type == 0 else '下级'
    return render(request, 'index.html', {'viids':viids})

def add(request):
    if request.method == "GET":
        return render(request, 'viid_add.html')
    elif request.method == "POST":
        post_dict = {'ipv6Addr':'','onlineStatus':2,'count':None,'opTime':None}
        try:
            post_dict.update({'deviceId':request.POST.get('deviceId').strip(), 'name':request.POST.get('name').strip(), 'userName':request.POST.get('userName').strip(), 'password':request.POST.get('password').strip(), 'ipAddr':request.POST.get('ipAddr').strip(), 'port':request.POST.get('port').strip(), 'type':request.POST.get('type').strip(), 'subscribeDetail':str(request.POST.getlist('subscribeDetail')).strip('[').strip(']').replace("'",''), 'receiveAddr':request.POST.get('receiveAddr').strip()})
            models.t_viid_system.objects.create(**post_dict)
            # viid = models.t_viid_system(post_dict)
            # viid.save()
            return redirect('/app01')
        except Exception as e:
            return HttpResponse('添加视图库错误：' + str(e))
            # return HttpResponse(str(request.body))


def edit(request):
    # todo
    return render(request, 'viid_edit.html')

def delete(request):
    # todo
    return render(request, 'index.html')
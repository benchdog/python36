#coding: utf8
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01 import models
from mysite import settings


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
    viid_list = models.t_viid_system.objects.all()
    for viid in viid_list:
        viid.onlineStatus = '在线' if viid.onlineStatus == 1 else '离线'
        viid.type = '上级' if viid.type == 0 else '下级'
    return render(request, 'index.html', {'viid_list':viid_list})

def add(request):
    if request.method == "GET":
        return render(request, 'viid_add.html')
    elif request.method == "POST":
        viid_dict = {'ipv6Addr': None, 'onlineStatus':2, 'count':None, 'opTime':None}
        try:
            viid_dict.update({'deviceId':request.POST.get('deviceId').strip(), 'name':request.POST.get('name').strip(), 'userName':request.POST.get('userName').strip(), 'password':request.POST.get('password').strip(), 'ipAddr':request.POST.get('ipAddr').strip(), 'port':request.POST.get('port').strip(), 'type':request.POST.get('type').strip(), 'subscribeDetail':str(request.POST.getlist('subscribeDetail')).strip('[').strip(']').replace("'", ''), 'receiveAddr':request.POST.get('receiveAddr').strip()})
            models.t_viid_system.objects.create(**viid_dict)
            # viid = models.t_viid_system(post_dict)
            # viid.save()
            return redirect('/app01')
        except Exception as e:
            return HttpResponse('添加视图库异常：' + str(e))
            # return HttpResponse(str(request.body))


def edit(request):
    if request.method == 'GET':
        try:
            # id = request.GET.get('id')
            # viid = models.t_viid_system.objects.filter(id = id)
            viid = models.t_viid_system.objects.get(id = request.GET.get('id'))
            # print(type(viid))
            viid.onlineStatus = '在线' if viid.onlineStatus == 1 else '离线'
            viid.type = '上级' if viid.type == 0 else '下级'
            return render(request, 'viid_edit.html', {'viid':viid})
        except Exception as e:
            return HttpResponse('编辑视图库异常：，' + str(e))
    elif request.method == 'POST':
        viid_dict = {'ipv6Addr': None, 'onlineStatus': 2, 'count': None, 'opTime': None}
        try:
            viid_dict.update(
                {'deviceId': request.POST.get('deviceId').strip(), 'name': request.POST.get('name').strip(),
                 'userName': request.POST.get('userName').strip(), 'password': request.POST.get('password').strip(),
                 'ipAddr': request.POST.get('ipAddr').strip(), 'port': request.POST.get('port').strip(),
                 'type': request.POST.get('type').strip(),
                 'subscribeDetail': str(request.POST.getlist('subscribeDetail')).strip('[').strip(']').replace("'", ''),
                 'receiveAddr': request.POST.get('receiveAddr').strip()})
            # models.t_viid_system.objects.create(**viid_dict)
            models.t_viid_system.objects.filter(id = request.POST.get('id')).update(**viid_dict)
            # return HttpResponse('---' + str(request.POST.get('id')) + '+++')
            return redirect('/app01')
        except Exception as e:
            return HttpResponse('编辑视图库异常：' + str(e))

def delete(request):
    if request.method == 'GET':
        models.t_viid_system.objects.get(id = request.GET.get('id')).delete()
        # models.t_viid_system.objects.filter(id = request.GET.get('id')).delete()
        return redirect('/app01')

def subscribe(request):
    if request.method == 'GET':
        try:
            viid = models.t_viid_system.objects.get(id = request.GET.get('id'))
            subscribe_list = models.t_subscribe.objects.filter(viidSystemID = request.GET.get('id'), subscribeStatus = 0)
            if subscribe_list:
                for subscribe in subscribe_list:
                    subscribe.type = '上级' if subscribe.type == 0 else '下级'
                    # for detail in subscribe.subscribeDetail.split(','):
                    #     if
            return render(request, 'subscribe.html', {'viid':viid, 'subscribe_list':subscribe_list})
        except Exception as e:
            return HttpResponse('订阅异常：，' + str(e))
        # return HttpResponse(request.GET.get('id'))
    # SUBSCRIBE_URL = settings.SUBSCRIBE_URL_PREFIX + str(request.GET.get('id'))
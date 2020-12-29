#coding: utf8
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
        # # post_dict = request.POST.getlist
        # return HttpResponse(request.POST)
        # return HttpResponse(str(post_dict))
        post_dict = request.POST
        try:
            viid = models.t_viid_system(post_dict)
            viid.save()
            return redirect('/app01')
        except Exception as e:
            return HttpResponse('error' + str(e))




def edit(request):
    # todo
    return render(request, 'viid_edit.html')

def delete(request):
    # todo
    return render(request, 'index.html')
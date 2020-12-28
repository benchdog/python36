#coding: utf8
from django.http import HttpResponse
from django.shortcuts import render
import sys

# Create your views here.

def index(request):
    return HttpResponse(sys.path)

def ape_stat(request):
    if request.method == 'GET':#GET区分大小写
        return render(request,'ape_stat.html')
        # return HttpResponse(BASE_DIR)
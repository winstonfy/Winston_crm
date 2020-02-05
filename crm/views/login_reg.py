#__author__ = 'Winston'
#date: 2020/1/9

from django.shortcuts import render,redirect,reverse
from django.contrib import auth
from crm.forms import RegForm
from crm import models
from django.http import JsonResponse
from rbac.server.init_permission import init_permission

def login(request):
    ret = {'status':0,'msg1':''}
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj=auth.authenticate(request,username=username,password=password)
        if obj:
            auth.login(request,obj)
            # 认证成功 初始化权限信息
            permission_ret=init_permission(request,obj)
            if permission_ret:
                ret['status'] = 1
                ret['msg1'] =permission_ret
            ret['url']=reverse('my_customer')
            return JsonResponse(ret)
        else:
            ret['status']=1
            ret['msg1']='用户名或密码错误'
            return JsonResponse(ret)

    return render(request, 'crm/login_reg/login.html')

def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop('re_password')
            models.UserProfile.objects.create_user(**form_obj.cleaned_data)
            return redirect('/login/')
    return render(request, 'crm/login_reg/reg.html', {'form_obj':form_obj})
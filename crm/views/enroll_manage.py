from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import auth
from crm.forms import RegForm, CustomerForm, ConsultRecordForm, EnrollmentForm
from crm import models
from django.http import JsonResponse, QueryDict
from utils.pagination import Pagination
from django.views import View
from django.db.models import Q
from django.db import transaction
from django.conf import settings


# 展示客户信息
class CustomerList(View):

    def get(self, request):
        q = self.get_search_contion(['qq', 'name'])

        if request.path_info == reverse('customer'):
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(q, consultant=request.user)
        # query_params =copy.deepcopy(request.GET)
        query_params = request.GET.copy()  # 深拷贝
        page = Pagination(request, all_customer.count(), query_params)

        query_params = self.get_add_btn()

        return render(request, 'crm/enroll_manage/customer_list.html',
                      {'all_customer': all_customer[page.start:page.end], 'pagination': page.show_li,
                       'query_params': query_params})

    def post(self, request):
        print(request.POST)
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        ret = getattr(self, action)()

        if ret:
            return ret

        return self.get(request)

    def multi_apply(self):
        # 公户变私户
        ids = self.request.POST.getlist('id')
        apply_num = len(ids)
        # 用户总数不能超过设置值
        if self.request.user.customers.count() + apply_num > settings.CUSTOMER_MAX_NUM:
            return HttpResponse('做人不要贪心 给别人点机会')

        with transaction.atomic():
            # 加锁
            obj_list = models.Customer.objects.filter(id__in=ids, consultant__isnull=True).select_for_update()
            if apply_num == len(obj_list):
                obj_list.update(consultant=self.request.user)
            else:
                return HttpResponse('客户已被其他销售抢走')

    def multi_pub(self):
        ids = self.request.POST.getlist('id')
        models.Customer.objects.filter(id__in=ids).update(consultant=None)

    def get_search_contion(self, query_list):

        query = self.request.GET.get('query', '')

        q = Q()
        q.connector = 'OR'
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        # Q(Q(qq__contains=query) |Q(name__contains=query))

        return q

    def get_add_btn(self):
        url = self.request.get_full_path()
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = url
        query_params = qd.urlencode()
        return query_params


# 新增和编辑客户
def customer(request, edit_id=None):
    obj = models.Customer.objects.filter(id=edit_id).first()
    form_obj = CustomerForm(instance=obj)
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('customer'))

    return render(request, 'crm/enroll_manage/customer.html', {'form_obj': form_obj, 'edit_id': edit_id})


# 展示跟进记录
class ConsultRecord(View):

    def get(self, request, customer_id):
        if customer_id == '0':
            all_consult_record = models.ConsultRecord.objects.filter(delete_status=False, consultant=request.user)
        else:
            all_consult_record = models.ConsultRecord.objects.filter(customer_id=customer_id, delete_status=False)

        return render(request, 'crm/enroll_manage/consult_record_list.html', {'all_consult_record': all_consult_record})


# 新增和编辑跟进记录

def consult_record(request, edit_id=None):
    obj = models.ConsultRecord.objects.filter(id=edit_id).first() or models.ConsultRecord(consultant=request.user)
    form_obj = ConsultRecordForm(instance=obj)
    if request.method == 'POST':
        form_obj = ConsultRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_record', args=(0,)))

    return render(request, 'crm/enroll_manage/consult_record.html', {'form_obj': form_obj, 'edit_id': edit_id})


# 展示报名记录
class EnrollmentList(View):

    def get(self, request, customer_id):
        if customer_id == '0':
            all_record = models.Enrollment.objects.filter(delete_status=False, customer__consultant=request.user)
        else:
            all_record = models.Enrollment.objects.filter(customer_id=customer_id, delete_status=False)

        query_params = self.get_query_params()

        return render(request, 'crm/enroll_manage/enrollment_list.html',
                      {'all_record': all_record, 'query_params': query_params})

    def get_query_params(self):
        url = self.request.get_full_path()
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = url
        query_params = qd.urlencode()
        return query_params


# 添加报名记录
def enrollment(request, customer_id=None, edit_id=None):
    obj = models.Enrollment.objects.filter(id=edit_id).first() or models.Enrollment(customer_id=customer_id)
    form_obj = EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            enrollment_obj = form_obj.save()
            enrollment_obj.customer.status = 'signed'
            enrollment_obj.customer.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect(reverse('my_customer'))

    return render(request, 'crm/enroll_manage/enrollment.html', {'form_obj': form_obj})

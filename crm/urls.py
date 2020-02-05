from django.conf.urls import url
from crm.views import enroll_manage,class_manage
urlpatterns = [
    # 招生管理
    # 客户展示
    url(r'^customer_list/', enroll_manage.CustomerList.as_view(),name='customer'),
    url(r'^my_customer/', enroll_manage.CustomerList.as_view(),name='my_customer'),
    url(r'^customer/add/', enroll_manage.customer,name='add_customer'),
    url(r'^customer/edit/(\d+)/', enroll_manage.customer,name='edit_customer'),
    # 跟进记录
    url(r'^consult_record_list/(\d+)/', enroll_manage.ConsultRecord.as_view(),name='consult_record'),
    url(r'^consult_record/add/', enroll_manage.consult_record,name='add_consult_record'),
    url(r'^consult_record/edit/(\d+)/', enroll_manage.consult_record,name='edit_consult_record'),
    # 报名记录
    url(r'^enrollment_list/(\d+)/', enroll_manage.EnrollmentList.as_view(),name='enrollment'),
    url(r'^enrollment/add/(\d+)/', enroll_manage.enrollment,name='add_enrollment'),
    url(r'^enrollment/edit/(\d+)/', enroll_manage.enrollment,name='edit_enrollment'),

    #班级管理
    #班级展示
    url(r'^class_list/', class_manage.ClassList.as_view(),name='class_list'),
    url(r'^class/add/', class_manage.classes,name='add_class'),
    url(r'^class/edit/(\d+)/', class_manage.classes,name='edit_class'),
    #课程记录
    url(r'^course_list/(\d+)/', class_manage.CourseList.as_view(),name='course_list'),
    url(r'^course/add/(?P<class_id>\d+)/', class_manage.course,name='add_course'),
    url(r'^course/edit/(?P<edit_id>\d+)/', class_manage.course,name='edit_course'),

    # 展示学习记录
    url(r'^study_record_list/(?P<course_id>\d+)/', class_manage.study_record,name='study_record_list'),
]

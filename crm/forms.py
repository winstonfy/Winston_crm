# __author__ = 'Winston'
# date: 2020/1/3

from django import forms
from crm import models
from django.core.exceptions import ValidationError


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control frominput'})


# 注册form
class RegForm(BaseForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.widgets.EmailInput(),
        error_messages={'required': '用户名不能为空',
                        'invalid': '邮箱格式不对',}
    )
    password = forms.CharField(
        label='密码',
        widget=forms.widgets.PasswordInput(),
        min_length=6,
        error_messages={'min_length': '最小长度为6',
                        'required': '密码不能为空'}
    )
    re_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(),
        error_messages={'required': '密码不能为空'}
    )

    class Meta:
        model = models.UserProfile
        fields = ['username', 'password', 're_password', 'name', 'department']  # 指定字段
        widgets = {
            'username': forms.widgets.EmailInput,
            'password': forms.widgets.PasswordInput,
        }
        labels = {
            'username': '用户名',
            'password': '密码',
            'name': '姓名',
            'department': '部门',
        }

        error_messages = {
            'name': {
                'required': '姓名不能为空'
            },
            'department': {
                'required': '部门不能为空'
            }
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_username_exist = models.UserProfile.objects.filter(username=username).exists()
        if is_username_exist:
            raise ValidationError("该用户名已存在")
        return username


    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')

# 客户form
class CustomerForm(BaseForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        widgets = {
            'course': forms.widgets.SelectMultiple
        }

        error_messages = {
            'qq': {
                'required': 'qq号不能为空'
            },
            'course': {
                'required': '咨询课程不能为空'
            }
        }


# 跟近记录form
class ConsultRecordForm(BaseForm):
    class Meta:
        model = models.ConsultRecord
        # fields = '__all__'
        exclude = ['delete_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customer_choice = [(i.id, i) for i in self.instance.consultant.customers.all()]
        customer_choice.insert(0, ('', '------'))
        # 限制客户是当前销售的私户
        self.fields['customer'].widget.choices = customer_choice
        # 限制跟进人是当前用户(销售)
        self.fields['consultant'].widget.choices = [(self.instance.consultant.id, self.instance.consultant), ]


# 报名表form
class EnrollmentForm(BaseForm):

    class Meta:
        model = models.Enrollment
        exclude = ['contract_approved','delete_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].widget.choices = [(self.instance.customer_id,
                                                  self.instance.customer),]
        self.fields['enrolment_class'].widget.choices = [(i.id,i) for i in self.instance.customer.class_list.all()]


# 班级form
class ClassForm(BaseForm):

    class Meta:
        model = models.ClassList
        fields = '__all__'

# 课程记录form
class CourseForm(BaseForm):

    class Meta:
        model = models.CourseRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 限制当前的班级是传过来id的班级
        self.fields['re_class'].widget.choices =[(self.instance.re_class_id,self.instance.re_class)]
        # 限制当前的班主任是当前用户
        self.fields['teacher'].widget.choices =[(self.instance.teacher_id,self.instance.teacher)]

# 学习记录form
class StudyRecordForm(BaseForm):

    class Meta:
        model = models.StudyRecord
        fields = ['attendance','score','homework_note','student']

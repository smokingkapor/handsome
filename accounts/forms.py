# -*- coding: utf-8 -*-
import re

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.cache import cache

from .models import Profile, Photo


class LoginForm(forms.Form):
    """
    Form for user login.
    """
    username = forms.CharField(
        label='用户名/手机号',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        """
        Check the username and password here
        """
        data = self.data
        username = data['username']
        password = data['password']

        if not auth.authenticate(username=username, password=password):
            raise forms.ValidationError('用户名或者密码错误，请重试')
        return data


class PhoneLoginForm(forms.Form):
    """
    Form for user login with phone
    """
    phone = forms.CharField(label=u'*手机号')
    password = forms.CharField(label=u'*动态密码')

    def clean_phone(self):
        """
        Check phone number
        """
        phone = self.data.get('phone')
        if not re.match('^1[3-9]\d{9}$', phone):
            raise forms.ValidationError(u'无效的手机号码')

        return phone

    def clean(self):
        """
        Check phone and password
        """
        data = self.data
        phone = data.get('phone')
        password = data.get('password')
#         if not Profile.objects.filter(phone=phone).exists():
#             raise forms.ValidationError(u'这个手机号暂未在优草注册使用')

        if password not in cache.get(u'pwds_{}'.format(phone), []):
            raise forms.ValidationError(u'动态密码错误')

        return data


class RegisterForm(forms.Form):
    """
    Create new account form
    """
    username = forms.CharField(
        label=u'*用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label=u'*密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label=u'*确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        required=False,
        label=u'邮箱',
        help_text=u'用于找回密码（可不填）',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        """
        Check if the user already exist
        """
        data = self.cleaned_data
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError(u'两次输入的密码不匹配')
        if User.objects.filter(username=data.get('username')).exists():
            raise forms.ValidationError('用户名已经存在，是不是忘记了密码？')
        return self.data


class UploadForm(forms.Form):
    """
    Form for uploading full body shot
    """
    file = forms.ImageField()


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file',)


class ProfileForm(forms.ModelForm):
    """
    Model form for update Profile model
    """
    class Meta:
        model = Profile
        fields = ('height', 'weight', 'clothing_size', 'pants_size', 'pants_style', 'age')


class UpdatePasswordForm(forms.Form):
    new_password = forms.CharField(label=u'新密码', widget=forms.PasswordInput)
    new_password_again = forms.CharField(label=u'确认新密码', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.data.get('new_password') != self.data.get('new_password_again'):
            raise forms.ValidationError(u'两次输入的新密码不匹配')

        if self.user.profile.is_random_user:
            new_username = self.data.get('new_username').strip()
            if self.user.username != new_username:
                if not new_username:
                    raise forms.ValidationError(u'新用户名不能为空')
                elif User.objects.filter(username=new_username):
                    raise forms.ValidationError(u'用户名已经被占用')
                else:
                    self.user.username = new_username
                    self.user.profile.is_random_user = False
                    self.user.profile.save()

        self.user.set_password(self.data.get('new_password'))
        self.user.save()
        return self.cleaned_data

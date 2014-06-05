# -*- coding: utf-8 -*-
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Profile
from django.core.validators import validate_integer


class LoginForm(forms.Form):
    """
    Form for user login.
    """
    username = forms.CharField(
        label='用户名',
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


class RegisterForm(forms.Form):
    """
    Create new account form
    """
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        """
        Check if the user already exist
        """
        username = self.data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已经存在，是不是忘记了密码？')
        return self.data


class UploadForm(forms.Form):
    """
    Form for uploading full body shot
    """
    file = forms.ImageField()


class ProfileForm(forms.ModelForm):
    """
    Model form for update Profile model
    """
    class Meta:
        model = Profile
        fields = ('height', 'weight', 'waistline', 'chest', 'hipline', 'foot')

    def _validate_field(self, field_name):
        value = self.cleaned_data.get(field_name)
        validate_integer(value)
        return value

    def clean_height(self):
        return self._validate_field('height')

    def clean_weight(self):
        return self._validate_field('weight')

    def clean_waistline(self):
        return self._validate_field('waistline')

    def clean_chest(self):
        return self._validate_field('chest')

    def clean_hipline(self):
        return self._validate_field('hipline')

    def clean_foot(self):
        return self._validate_field('foot')

# -*- coding: utf-8 -*-
import json
import string
from datetime import datetime

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponse
from django.views.generic.base import RedirectView, View, TemplateView
from django.views.generic.edit import FormView, CreateView
from django.utils.crypto import get_random_string

from braces.views import(
    LoginRequiredMixin, CsrfExemptMixin, AjaxResponseMixin,
    JsonRequestResponseMixin
)

from .forms import(
    LoginForm, RegisterForm, ProfileForm, PhoneLoginForm,
    PhotoForm, UpdatePasswordForm
)
from .models import Profile, Photo
from handsome.utils import send_sms


class LoginView(FormView):
    """
    View for user sign in.
    """
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get_success_url(self):
        """
        Check if next param exist
        """
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse('portals:index')

    def get_context_data(self, **kwargs):
        """
        Add extra data to the context
        """
        data = super(LoginView, self).get_context_data(**kwargs)
        data.update({'query_string': self.request.META['QUERY_STRING']})
        return data

    def form_valid(self, form):
        """
        Login current user.
        """
        data = form.cleaned_data
        user = auth.authenticate(username=data['username'],
                                 password=data['password'])
        auth.login(self.request, user)

        return super(LoginView, self).form_valid(form)


class PhoneLoginView(FormView):
    """
    Allow the user to login with phone
    """
    template_name = 'accounts/phone_login.html'
    form_class = PhoneLoginForm

    def get_success_url(self):
        """
        Check if next param exist
        """
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse('portals:index')

    def get_context_data(self, **kwargs):
        """
        Add extra data to the context
        """
        data = super(PhoneLoginView, self).get_context_data(**kwargs)
        data.update({'query_string': self.request.META['QUERY_STRING']})
        return data

    def form_valid(self, form):
        """
        Login the user here
        """
        phone = form.cleaned_data['phone']
        if not Profile.objects.filter(phone=phone).exists():
            user = User.objects.create_user(username=phone)
            user.profile.phone = phone
            user.profile.save()
        else:
            user = Profile.objects.filter(phone=phone).order_by('-user__date_joined')[0].user  # noqa
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(self.request, user)
        return super(PhoneLoginView, self).form_valid(form)


class SendTemporaryPasswordView(AjaxResponseMixin, JsonRequestResponseMixin,
                                View):
    """
    Send temporary password to the cell phone.
    Only one temporary password will be sent in one minute.
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Send password
        """
        phone = request.REQUEST['phone']
        last_sent = cache.get(u'pwd_last_sent_{}'.format(phone))
        if not last_sent or (datetime.now()-last_sent).total_seconds() >= 60:
            pwds = cache.get(u'pwds_{}'.format(phone), [])
            new_pwd = get_random_string(6, string.digits)
            send_sms(phone,
                     settings.SMS_TEMPLATES['temporary_pwd'].format(new_pwd))
            pwds.append(new_pwd)
            cache.set(u'pwds_{}'.format(phone), pwds, 1800)

        return self.render_json_response({'success': True})


class LogoutView(RedirectView):
    """
    Logout current user and redirect to sign in page
    """
    permanent = False
    url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        """
        Logout here
        """
        auth.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(FormView):
    """
    Register a new account
    """
    form_class = RegisterForm
    template_name = 'accounts/register.html'

    def get_success_url(self):
        """
        Check if next param exist
        """
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse('portals:index')

    def form_valid(self, form):
        """
        Create account.
        """
        data = form.cleaned_data
        user = User(username=data['username'])
        user.set_password(data['password'])
        user.save()

        # login the user
        user = auth.authenticate(username=data['username'],
                                 password=data['password'])
        auth.login(self.request, user)

        return super(RegisterView, self).form_valid(form)


class CreateRandomUserView(RedirectView):
    """
    Create a random user and login the user
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Create user here
        """
        next_url = self.request.GET.get('next')
        if not next_url:
            return reverse('accounts:register')

        if not self.request.user.is_authenticated():
            username = 'random_user_' + get_random_string(5)
            password = get_random_string()
            user = User.objects.create_user(username=username,
                                            password=password)
            user.profile.is_random_user = True
            user.profile.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(self.request, user)

        return next_url


class CreatePhotoView(CsrfExemptMixin, LoginRequiredMixin, CreateView):
    """Create user photo"""
    model = Photo
    form_class = PhotoForm

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save()
        return HttpResponse(json.dumps({
            'success': True,
            'path': photo.file.get_thumbnail({'size': (128, 128)}).url,
            'id': photo.id}))

    def form_invalid(self, form):
        return HttpResponse(json.dumps({'success': False}))


class RemovePhotoView(LoginRequiredMixin, AjaxResponseMixin,
                      JsonRequestResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        photo = Photo.objects.get(id=request.GET['id'])
        if photo.user == request.user:
            photo.file.delete()
            photo.delete()
        return self.render_json_response({'success': True})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class UpdateProfileView(LoginRequiredMixin, AjaxResponseMixin,
                        JsonRequestResponseMixin, FormView):
    form_class = ProfileForm
    template_name = 'accounts/update_profile.html'

    def post_ajax(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, instance=self.request.user.profile)
        form.save()
        return self.render_json_response({'success': True,
                                          'next': reverse('accounts:profile')})

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(UpdateProfileView, self).get_context_data(**kwargs)
        data.update({
            'AGE_GROUP_CHOICES': Profile.AGE_GROUP_CHOICES,
            'CLOTHING_SIZE_CHOICES': Profile.CLOTHING_SIZE_CHOICES,
            'PANTS_SIZE_CHOICES': Profile.PANTS_SIZE_CHOICES,
            'PANTS_STYLE_CHOICES': Profile.PANTS_STYLE_CHOICES,
            'SHOE_SIZE_CHOICES': Profile.SHOE_SIZE_CHOICES,
            'COLOR_CHOICES': Profile.COLOR_CHOICES,
        })
        return data


class UpdatePasswordView(LoginRequiredMixin, FormView):
    form_class = UpdatePasswordForm
    template_name = 'accounts/update_password.html'
    success_url = reverse_lazy('accounts:update_password')

    def get_form(self, form_class):
        return form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        messages.success(self.request, u'密码修改成功')
        return super(UpdatePasswordView, self).form_valid(form)


class DesignerCaseView(TemplateView):
    template_name = 'accounts/case.html'

    def get_context_data(self, **kwargs):
        data = super(DesignerCaseView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])
        data.update({
            'cases': user.designerwork_set.all(),
            'designer': user.profile
        })
        return data

# -*- coding: utf-8 -*-
import json
import os

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from braces.views import JSONResponseMixin, LoginRequiredMixin, CsrfExemptMixin

from .forms import LoginForm, RegisterForm, UploadForm
from django.http.response import HttpResponse


class LoginView(JSONResponseMixin, FormView):
    """
    View for user sign in.
    """
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('portals:index')

    def form_valid(self, form):
        """
        Login current user.
        """
        data = form.cleaned_data
        user = auth.authenticate(username=data['username'],
                                 password=data['password'])
        auth.login(self.request, user)

        if self.request.is_ajax():
            return self.render_json_response({'success': True})
        else:
            return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Form is invalid
        """
        if self.request.is_ajax():
            return self.render_json_response(
                {'success': False, 'errors': form.non_field_errors()})
        else:
            return self.render_to_response(self.get_context_data(form=form))


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


class RegisterView(JSONResponseMixin, FormView):
    """
    Register a new account
    """
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

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

        if self.request.is_ajax():
            return self.render_json_response({'success': True})
        else:
            return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Form is invalid
        """
        if self.request.is_ajax():
            return self.render_json_response(
                {'success': False, 'errors': form.non_field_errors()})
        else:
            return self.render_to_response(self.get_context_data(form=form))


class UploadView(CsrfExemptMixin, LoginRequiredMixin, FormView):
    """
    Form view for uploading full body shot.
    """
    form_class = UploadForm

    def form_valid(self, form):
        """
        Upload shot to temple folder
        """
        data = form.cleaned_data
        name, ext = os.path.splitext(data['file'].name)
        filename = '{}{}'.format(self.request.user.id, ext)
        path = os.path.join(settings.MEDIA_ROOT, 'tmp', filename)
        if os.path.exists(path):
            os.remove(path)
        default_storage.save(path, ContentFile(data['file'].read()))
        path = '{}tmp/{}'.format(settings.MEDIA_URL, filename)
        return HttpResponse(json.dumps({'success': True, 'path': path}))

    def form_invalid(self, form):
        return HttpResponse(json.dumps({'success': False}))

# -*- coding: utf-8 -*-
import json
import os

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponse
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from braces.views import(
    JSONResponseMixin, LoginRequiredMixin, CsrfExemptMixin
)
from easy_thumbnails.files import get_thumbnailer

from .forms import LoginForm, RegisterForm, UploadForm, ProfileForm
from handsome.utils import generate_str


class LoginView(JSONResponseMixin, FormView):
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
        user = self.request.user
        name, ext = os.path.splitext(data['file'].name)
        filename = '{}.{}.{}'.format(user.id, generate_str(5), ext)
        root = os.path.join(settings.MEDIA_ROOT, 'tmp')
        path = os.path.join(root, filename)
        default_storage.save(path, ContentFile(data['file'].read()))
        thumbnailer = get_thumbnailer(u'tmp/{}'.format(filename))
        return HttpResponse(json.dumps({
            'success': True,
            'path': thumbnailer.get_thumbnail({'size': (256, 256)}).url,
            'filename': filename}))

    def form_invalid(self, form):
        return HttpResponse(json.dumps({'success': False}))


class UpdateProfileView(LoginRequiredMixin, FormView):
    """
    Update profile
    """
    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'

    def get_success_url(self):
        """
        Check if next param exist in the query string.
        """
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse('portals:index')

    def get_form_kwargs(self):
        """
        Add user profile to the form
        """
        kwargs = super(UpdateProfileView, self).get_form_kwargs()
        kwargs.update({'instance': self.request.user.profile})
        return kwargs

    def form_valid(self, form):
        """
        Save profile
        """
        form.save()
        return super(UpdateProfileView, self).form_valid(form)

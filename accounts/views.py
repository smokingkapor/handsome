# -*- coding: utf-8 -*-
import json
import os
import shutil

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.views.generic.base import RedirectView, View
from django.views.generic.edit import FormView

from braces.views import(
    JSONResponseMixin, LoginRequiredMixin, CsrfExemptMixin, AjaxResponseMixin
)
from easy_thumbnails.files import get_thumbnailer

from .forms import LoginForm, RegisterForm, UploadForm
from .models import Photo
from handsome.utils import generate_str


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
            profile_json = json.loads(serializers.serialize('json', [user.profile]))[0]['fields']  # noqa
            profile_json['url'] = user.profile.get_fullbody_shot_url()
            return self.render_json_response({'success': True,
                                              'profile': profile_json})
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


class UpdateView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin,
                 View):
    """
    Update personal info
    """
    def post_ajax(self, request, *args, **kwargs):
        """
        Update user profile
        """
        user = self.request.user
        profile = user.profile
        profile.preferred_style = request.POST['style']
        profile.age_group = request.POST['age_group']
        profile.height = request.POST['height']
        profile.weight = request.POST['weight']
        profile.waistline = request.POST['waistline']
        profile.chest = request.POST['chest']
        profile.hipline = request.POST['hipline']
        profile.foot = request.POST['foot']
        profile.save()

        # save full body shot
        filename = request.POST['filename']
        name, ext = os.path.splitext(filename)
        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'tmp', filename)

        fullbody_shot_root = os.path.join(settings.MEDIA_ROOT, 'fullbody-shot')
        if not os.path.exists(fullbody_shot_root):
            os.makedirs(fullbody_shot_root)

        if filename and os.path.exists(temp_file_path):
            new_filename = 'user_{}_{}{}'.format(user.id, generate_str(6), ext)
            fullbody_shot_path = os.path.join(fullbody_shot_root, new_filename)
            shutil.copy(temp_file_path, fullbody_shot_path)
            user.photo_set.update(is_primary=False)
            Photo(user=user,
                  file=u'fullbody-shot/{}'.format(new_filename),
                  is_primary=True).save()

        return self.render_json_response({'success': True})

# -*- coding: utf-8 -*-
import json
import os
import shutil

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseForbidden
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from braces.views import(
    StaffuserRequiredMixin, CsrfExemptMixin, AjaxResponseMixin,
    JSONResponseMixin, LoginRequiredMixin
)

from .forms import DesignForm
from .models import Design
from handsome.utils import generate_str
from orders.constants import DESIGNED
from orders.models import Order
from designs.models import DesignPhoto


class CreateDesignView(StaffuserRequiredMixin, AjaxResponseMixin,
                       JSONResponseMixin, CreateView):
    """
    Create design for client order
    """
    model = Design
    form_class = DesignForm

    def get_context_data(self, **kwargs):
        """
        Override. Add extra data to context
        """
        data = super(CreateDesignView, self).get_context_data(**kwargs)
        data.update(self.request.GET.dict())
        return data

    def form_valid(self, form):
        """
        Override. Create design and save photos
        """
        order = Order.objects.get(pk=self.request.GET['order'])
        design = form.save(commit=False)
        design.order = order
        design.designer = self.request.user
        design.client = order.creator
        design.save()
        order.status = DESIGNED
        order.save()

        # save photos
        for filename in form.cleaned_data['photos'].split(';'):
            name, ext = os.path.splitext(filename)
            temp_file_path = os.path.join(settings.MEDIA_ROOT, 'tmp', filename)

            design_photo_root = os.path.join(settings.MEDIA_ROOT, 'design-photo')  # noqa
            if not os.path.exists(design_photo_root):
                os.makedirs(design_photo_root)

            if filename and os.path.exists(temp_file_path):
                new_filename = 'design_{}_{}{}'.format(design.id, generate_str(6), ext)  # noqa
                design_photo_path = os.path.join(design_photo_root, new_filename)
                shutil.copy(temp_file_path, design_photo_path)
                photo = DesignPhoto(designer=self.request.user, file=new_filename)
                photo.save()
                design.photos.add(photo)

        if self.request.is_ajax():
            url = reverse('designs:detail', kwargs={'pk': design.id})
            return self.render_json_response({'success': True, 'next': url})

        return super(CreateDesignView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Override. Return JSON if it's AJAX.
        """
        if self.request.is_ajax():
            return self.render_json_response({'success': False})
        return super(CreateDesignView, self).form_invalid(form)


class UploadView(CsrfExemptMixin, StaffuserRequiredMixin, View):
    """
    Form view for uploading design photos
    """
    def post(self, request, *args, **kwargs):
        """
        Upload shot to temple folder
        """
        order = Order.objects.get(pk=request.GET['order'])
        user = self.request.user
        photo = request.FILES['file']
        name, ext = os.path.splitext(photo.name)
        filename = '{}.{}.{}{}'.format(user.id, order.id, generate_str(5), ext)
        root = os.path.join(settings.MEDIA_ROOT, 'tmp')
        path = os.path.join(root, filename)
        default_storage.save(path, ContentFile(photo.read()))
        url_path = '{}tmp/{}'.format(settings.MEDIA_URL, filename)
        return HttpResponse(json.dumps({'success': True, 'path': url_path,
                                        'filename': filename}))


class DesignDetailView(LoginRequiredMixin, DetailView):
    """
    Check the design
    """
    model = Design

    def dispatch(self, request, *args, **kwargs):
        """
        Override. Only the designers and the client can see the design
        """
        response = super(DesignDetailView, self).dispatch(request, *args, **kwargs)
        if not self.request.user.is_staff or self.request.user != self.object.client:
            return HttpResponseForbidden()
        return response

# -*- coding: utf-8 -*-
import json
import os
import shutil

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.views.generic.base import View, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from braces.views import(
    StaffuserRequiredMixin, CsrfExemptMixin, AjaxResponseMixin,
    JSONResponseMixin, LoginRequiredMixin
)

from .constants import SELECTED, REJECTED
from .forms import DesignForm, RejectDesignForm
from .mixins import DesignPermissionMixin
from .models import Design, DesignClothing
from clothings.models import Clothing
from designs.models import DesignPhoto
from handsome.utils import generate_str
from orders.constants import DESIGNED, ACCEPTED, PREPAID
from orders.models import Order


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
        data.update({'clothing_choices': Clothing.CATEGORY_CHOICES})
        return data

    def form_valid(self, form):
        """
        Override. Create design and save photos
        """
        order = Order.objects.get(code=self.request.GET['order'])
        design = form.save(commit=False)
        design.order = order
        design.designer = self.request.user
        design.client = order.creator
        design.save()

        # clothings
        for clothing in json.loads(form.cleaned_data['selected_clothings']):
            design_clothing = DesignClothing(clothing=Clothing.objects.get(pk=clothing['id']))
            design_clothing.size = clothing['size']
            design_clothing.color = clothing['color']
            design_clothing.save()
            design.clothings.add(design_clothing)

        # order
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
            url = reverse('designs:detail', kwargs={'code': design.code})
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
        order = Order.objects.get(code=request.GET['order'])
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


class DesignDetailView(LoginRequiredMixin, DesignPermissionMixin, DetailView):
    """
    Check the design
    """
    model = Design
    slug_field = 'code'
    slug_url_kwarg = 'code'


class AcceptDesignView(LoginRequiredMixin, DesignPermissionMixin, RedirectView):
    """
    Accept design
    """
    required_roles = ['owner']
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Update design here
        """
        design = Design.objects.get(code=kwargs['code'])
        design.status = SELECTED
        design.save()
        design.order.status = ACCEPTED
        design.order.save()
        return reverse('orders:detail', kwargs={'code': design.order.code})


class RejectDesignView(LoginRequiredMixin, DesignPermissionMixin, UpdateView):
    """
    Reject design
    """
    required_roles = ['owner']
    slug_field = 'code'
    slug_url_kwarg = 'code'
    form_class = RejectDesignForm
    model = Design

    def form_valid(self, form):
        """
        Update design and order status
        """
        design = form.save(commit=False)
        design.status = REJECTED
        design.save()
        design.order.status = PREPAID
        design.order.save()
        return super(RejectDesignView, self).form_valid(form)

    def get_success_url(self):
        return reverse('orders:detail',
                       kwargs={'code': self.object.order.code})

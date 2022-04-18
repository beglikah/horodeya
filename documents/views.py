import os

from django.shortcuts import redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings

from rules.contrib.views import AutoPermissionRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.views import generic
from documents.models import Document
from documents.forms import DocumentForm, DocumentUpdateForm


# Create your views here.
class DocumentsList(generic.ListView):
    model = Document
    template_name = 'documents/documents_list.html'

    def handle_no_permission(self):
        return redirect('permission_denied')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/ligin/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DocumentDetails(generic.DetailView):
    model = Document
    template_name = 'documents/document_details'

    def handle_no_permission(self):
        return redirect('permission_denied')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/ligin/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DocumentCreate(AutoPermissionRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm

    def handle_no_permission(self):
        return redirect('permission_denied')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def form_valid(self, form):
        user = self.request.user
        document = form.instance
        return super().form_valid(form)


class DocumentUpdate(AutoPermissionRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        document = form.instance
        if document.author != user:
            form.add_error(
                'document',
                "This document is not uploaded from you. You can't change it! "
            )
            return super().form_invalid(form)
        return super().form_valid(form)


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/pdf')
            cont = 'inline; filename=' + os.path.basename(file_path)
            response['Content-Disposition'] = cont
            return response
        raise Http404

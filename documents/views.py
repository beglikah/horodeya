from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from rules.contrib.views import LoginRequiredMixin, AutoPermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView

from django.views import generic
from documents.models import Document
from documents.forms import DocumentForm


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


class DocumentCreate(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'home/upload_file.html'
    success_url = '/documents/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.author = self.request.user
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DocumentUpdate(AutoPermissionRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'home/upload_file.html'

    def handle_no_permission(self):
        return redirect('permission_denied')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

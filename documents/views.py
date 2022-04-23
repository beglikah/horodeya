from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from rules.contrib.views import LoginRequiredMixin, AutoPermissionRequiredMixin
from django.contrib.auth.decorators import login_required
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


@login_required
def upload_doc(request):
    user = request.user
    print(user)
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)  # Do not forget to add: request.FILES
        if form.is_valid():
            # Do something with our files or simply save them
            # if saved, our files would be located in media/ folder under the project's base folder
            print(form)
            form.save()
            return redirect('/documents/')
            # return HttpResponse('The file is saved')
        else:
            form = DocumentForm()
            context = {
                'form': form,
            }
            return render(request, 'documents/document_form.html', context)
    return redirect('/documents/')


class DocumentCreate(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    success_url = '/documents/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/ligin/')
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
        user = self.request.user
        form.instance.author = self.request.user
        doc = form.instance
        form.save()
        return super().form_valid(form)


class DocumentUpdate(AutoPermissionRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentForm

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

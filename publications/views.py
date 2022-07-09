from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView

from publications.forms import PublicationForm
from publications.models import Publication
from publications.services import publication_list_service, publication_create_service


class PublicationListView(ListView):
    template_name = 'publications/publication_list.html'
    model = Publication
    context_object_name = 'publications'

    def get_queryset(self):
        return publication_list_service()


class PublicationCreateView(CreateView):
    template_name = 'publications/publication_create.html'
    model = Publication
    context_object_name = 'publication'
    form_class = PublicationForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            publication_create_service(user=self.request.user, **form.cleaned_data)
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.request.user.pk})


class PublicationDetailView(DetailView):
    template_name = 'publications/publication_detail.html'
    model = Publication
    context_object_name = 'publication'

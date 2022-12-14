from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from publications.forms import PublicationForm
from publications.models import Publication
from publications.services import publication_list_service, publication_create_service, publication_update_service


class PublicationListView(ListView):
    template_name = 'publications/publication_list.html'
    model = Publication
    context_object_name = 'publications'

    def get_queryset(self):
        return publication_list_service()


class PublicationCreateView(LoginRequiredMixin, CreateView):
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


class PublicationUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'publications/publication_update.html'
    model = Publication
    context_object_name = 'publication'
    form_class = PublicationForm

    def test_func(self):
        return self.request.user == self.get_object().user and self.get_object().moderation_status != 'INVALID'

    def get_success_url(self):
        return reverse('publications:publication_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        publication_update_service(publication=self.object, **form.cleaned_data)
        return redirect(self.get_success_url())


class PublicationDeleteView(UserPassesTestMixin, DeleteView):
    model = Publication

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.user.pk})


class PublicationListToModerate(UserPassesTestMixin, ListView):
    template_name = 'publications/publication_list_to_moderate.html'
    model = Publication
    context_object_name = 'publications'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return publication_list_service(moderation_status='NOT_MODERATED')


class PublicationDetailToModerateView(UserPassesTestMixin, DetailView):
    template_name = 'publications/publication_detail.html'
    model = Publication
    context_object_name = 'publication'

    def test_func(self):
        return self.request.user.is_staff


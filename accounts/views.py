from django.shortcuts import render

# Create your views here.

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from accounts.forms import MyUserCreationForm
from publications.services import publication_list_service


class LoginUserView(LoginView):
    template_name = 'accounts/registration/login.html'
    # redirect_authenticated_user = True


class RegisterView(CreateView):
    model = get_user_model()
    template_name = 'accounts/registration/user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:login')


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['filtered_publications'] = publication_list_service(user=self.get_object(), moderation_status='VALID')
        return context

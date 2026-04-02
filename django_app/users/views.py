from django.views.generic import DetailView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterForm
from .models import Profile

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

class ProfileView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.kwargs['user_id'])
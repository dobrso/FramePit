from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RoomForm
from .models import Room

class RoomsListView(ListView):
    model = Room
    template_name = 'rooms/rooms_list.html'

class RoomCreateView(CreateView, LoginRequiredMixin):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_create.html'
    success_url = reverse_lazy('main:home')

class RoomDetailView(DetailView, LoginRequiredMixin):
    model = Room
    template_name = 'rooms/room_detail.html'

class RoomUpdateView(UpdateView, LoginRequiredMixin):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_update.html'

class RoomDeleteView(DeleteView, LoginRequiredMixin):
    model = Room
    template_name = 'rooms/room_delete.html'
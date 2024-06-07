from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Task
from django.urls import reverse_lazy

# Create your views here.

class TaskList(ListView):
  template_name = 'list.html'
  model = Task

class TaskDetail(DetailView):
  template_name = 'detail.html'
  model = Task

class TaskCreate(CreateView):
  template_name = 'create.html'
  model = Task
  fields = ('task_name', 'status_id')
  success_url = reverse_lazy('list')

class TaskDelete(DeleteView):
  template_name = 'delete.html'
  model = Task
  success_url = reverse_lazy('list')

class TaskUpdate(UpdateView):
  template_name = 'update.html'
  model = Task
  fields = ('task_name', 'status_id')
  success_url = reverse_lazy('list')
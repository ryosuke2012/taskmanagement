from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Task

# Create your views here.

class TaskList(ListView):
  template_name = 'list.html'
  model = Task

class TaskDetail(DetailView):
  template_name = 'detail.html'
  model = Task
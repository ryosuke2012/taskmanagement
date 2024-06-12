from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy

# Create your views here.

def TaskList(request):
  tasks = Task.objects.all()
  return render(request, 'list.html', {'tasks': tasks})

def TaskDetail(request, pk):
  task = get_object_or_404(Task, pk=pk)
  return render(request, 'detail.html', {'task': task})

def TaskCreate(request):
  if request.method == 'POST':
    form = TaskForm(request.POST)
    if form.is_valid():
      task = form.save(commit=False)
      task.save()
      return redirect('list')
  else:
    form = TaskForm()
    return render(request, 'form.html', {'form': form})

def TaskDelete(request, pk):
  task = get_object_or_404(Task, pk=pk)
  task.deleted_flg = True
  task.save()
  return redirect('list')

def TaskUpdate(request, pk):
  task = get_object_or_404(Task, pk=pk)
  if request.method == 'POST':
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
      form.save()
      return redirect('list')
  else:
    form = TaskForm(instance=task)
  return render(request, 'form.html', {'form': form})

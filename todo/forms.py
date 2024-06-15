from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['task_name', 'status_id', 'end_date']
  
  def clean_task_name(self):
    task_name = self.cleaned_data.get('task_name')
    if not task_name:
      raise forms.ValidationError('タスク名は必須です。')
    return task_name
  
  def clean_status_id(self):
    status_id = self.cleaned_data.get('status_id')
    if not status_id:
      raise forms.ValidationError('ステータスは必須です。')
    return status_id
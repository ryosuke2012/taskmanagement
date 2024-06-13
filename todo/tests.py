from django.test import TestCase
from django.urls import reverse
from .forms import TaskForm
from .models import Task, Status

class TaskFormTests(TestCase):
  
  def setUp(self):
    self.status = Status.objects.create(status='未着手')

  def test_valid_when_given_task_name_and_status_id(self):
    data = {
      'task_name': 'Test Task',
      'status_id': self.status.id
    }
    task = Task()
    form =TaskForm(data, instance=task)
    self.assertTrue(form.is_valid())

  def test_valid_when_not_given_start_date(self):
    data = {
      'task_name': 'Test Task',
      'status_id': self.status.id
    }
    task = Task()
    task.start_date = None
    form =TaskForm(data, instance=task)
    self.assertTrue(form.is_valid())

  def test_valid_when_not_given_end_date(self):
    data = {
      'task_name': 'Test Task',
      'status_id': self.status.id
    }
    task = Task()
    task.end_date = None
    form =TaskForm(data, instance=task)
    self.assertTrue(form.is_valid())

  def test_invalid_when_not_given_task_name(self):
    data = {
      'task_name': '',
      'status_id': self.status.id
    }
    task = Task()
    form =TaskForm(data, instance=task)
    self.assertFalse(form.is_valid())

  def test_invalid_when_task_name_null(self):
    data = {
      'status_id': self.status.id
    }
    task = Task()
    form =TaskForm(data, instance=task)
    self.assertFalse(form.is_valid())

  def test_invalid_when_not_given_status_id(self):
    data = {
      'task_name': 'Test Task',
      'status_id': ''
    }
    task = Task()
    form =TaskForm(data, instance=task)
    self.assertFalse(form.is_valid())

  def test_invalid_when_status_id_null(self):
    data = {
      'task_name': 'Test Task'
    }
    task = Task()
    form =TaskForm(data, instance=task)
    self.assertFalse(form.is_valid())
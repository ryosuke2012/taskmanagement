from django.test import TestCase
from django.urls import reverse
from .forms import TaskForm
from .models import Task, Status
import datetime
from django.shortcuts import get_object_or_404
from django.http import Http404

class TaskCreateTests(TestCase):
  
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
    self.assertEqual(task.task_name, 'Test Task')

  def test_valid_when_not_given_start_date(self):
    data = {
      'task_name': 'Test Task',
      'status_id': self.status.id
    }
    task = Task()
    task.start_date = None
    form = TaskForm(data, instance=task)
    self.assertTrue(form.is_valid())
    self.assertIsNone(task.start_date)

  def test_valid_when_not_given_end_date(self):
    data = {
      'task_name': 'Test Task',
      'status_id': self.status.id
    }
    task = Task()
    task.end_date = None
    form =TaskForm(data, instance=task)
    self.assertTrue(form.is_valid())
    self.assertIsNone(task.end_date)

  def test_invalid_when_not_given_task_name(self):
    data = {
      'task_name': '',
      'status_id': self.status.id
    }
    task = Task()
    form =TaskForm(data, instance=task)
    self.assertFalse(form.is_valid())
    self.assertEqual(task.task_name, '')

  def test_invalid_when_task_name_null(self):
    data = {
      'task_name': None,
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

class TaskGetListDetailTest(TestCase):
  def setUp(self):
    self.status_not_started = Status.objects.create(status='未着手')
    self.status_completed = Status.objects.create(status='完了')
    d = datetime.datetime.now()
    s_date = d.date()
    e_date = d.date()
    self.task1 = Task.objects.create(
      task_name='Test Task1',
      status_id=self.status_not_started,
      start_date=s_date,
      end_date=e_date
    )

    self.task2 = Task.objects.create(
      task_name='Test Task2',
      status_id=self.status_not_started
    )

  def test_get_task_list(self):
    response = self.client.get(reverse('list'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.task1.task_name)
    self.assertContains(response, self.task2.task_name)

  def test_get_task_detail_by_id(self):
    response = self.client.get(reverse('detail', kwargs={'pk': self.task1.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.task1.task_name)

  def test_get_task_detail_by_task_name(self):
    response = self.client.get(reverse('detail', kwargs={'pk': self.task1.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.task1.task_name)
    self.assertNotContains(response, self.task2.task_name)

  def test_get_task_detail_by_status_id(self):
    response = self.client.get(reverse('detail', kwargs={'pk': self.task1.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.task1.status_id)

  # 作成日が検索条件に入力されている
  # def test_get_task_detail_by_start_date(self):

  # 完了日が検索条件に入力されている
  # def test_get_task_detail_by_end_date(self):

  def test_get_task_detail_with_null_id(self):
    with self.assertRaises(Http404):
      task = get_object_or_404(Task, id=None)

  # タスク名がnullの場合
  # def test_get_list_with_null_task_name(self):

  # タスク状況がnullの場合
  # def test_get_list_with_null_status_id(self):


class TaskUpdateTests(TestCase):
  def setUp(self):
    self.status_not_started = Status.objects.create(status='未着手')
    self.status_completed = Status.objects.create(status='完了')

    self.task = Task.objects.create(
      task_name = 'Test Task',
      status_id = self.status_not_started,
      end_date  = None
    )

  def test_update_task_name_and_status_id(self):
    data = {
      'task_name': 'Updated Task',
      'status_id': self.status_completed.id
    }
    response = self.client.post(reverse('update', kwargs={'pk': self.task.pk}), data)
    self.assertEqual(response.status_code, 302)
    updated_task = Task.objects.get(pk=self.task.pk)
    self.assertEqual(updated_task.task_name, 'Updated Task')
    self.assertEqual(updated_task.status_id.status, '完了')

  def test_update_task_with_empty_end_date(self):
    data = {
      'task_name': 'Test Task',
      'status_id': self.status_not_started.id,
      'end_date' : ''
    }
    response = self.client.post(reverse('update', kwargs={'pk': self.task.pk}), data)
    self.assertEqual(response.status_code, 302)
    updated_task = Task.objects.get(pk=self.task.pk)
    self.assertIsNone(updated_task.end_date)

  def test_update_task_with_end_date(self):
    d = datetime.datetime.now()
    end_date = d.date()
    data = {
      'task_name': 'Updated Task',
      'status_id': self.status_completed.id,
      'end_date': end_date
    }
    response = self.client.post(reverse('update', kwargs={'pk': self.task.pk}), data)
    self.assertEqual(response.status_code, 302)
    updated_task = Task.objects.get(pk=self.task.pk)
    self.assertAlmostEqual(updated_task.end_date, end_date)

  def test_update_task_with_task_name_null(self):
    data = {
      # 'task_name': None,
      'status_id': self.status_not_started.id
    }
    response = self.client.post(reverse('update', kwargs={'pk': self.task.pk}), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'form.html')
    form = response.context['form']
    self.assertFalse(form.is_valid())
    self.assertIn('task_name', form.errors)
    self.assertEqual(form.errors['task_name'], ['このフィールドは必須です。'])

  def test_update_task_with_empty_task_name(self):
    data = {
      'task_name': '',
      'status_id': self.status_not_started.id
    }
    response = self.client.post(reverse('update', kwargs={'pk': self.task.pk}), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'form.html')
    form = response.context['form']
    self.assertFalse(form.is_valid())
    self.assertIn('task_name', form.errors)
    self.assertEqual(form.errors['task_name'], ['このフィールドは必須です。'])

  def test_update_task_with_status_id_null(self):
    data = {
      'task_name': 'Updated task',
      # 'status_id': None
    }
    response = self.client.post(reverse('update', kwargs={'pk': self.task.pk}), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'form.html')
    form = response.context['form']
    self.assertFalse(form.is_valid())
    self.assertIn('status_id', form.errors)
    self.assertEqual(form.errors['status_id'], ['このフィールドは必須です。'])

  def test_update_task_with_empty_status_id(self):
    data = {
      'task_name': 'Updated task',
      'status_id': ''
    }
    response = self.client.post(reverse('update', kwargs={'pk': self.task.pk}), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'form.html')
    form = response.context['form']
    self.assertFalse(form.is_valid())
    self.assertIn('status_id', form.errors)
    self.assertEqual(form.errors['status_id'], ['このフィールドは必須です。'])

  def test_update_with_different_task_id(self):
    nonexistent_id = self.task.id + 1
    data = {
      'task_name': 'Updated task',
      'status_id': self.status_not_started.id
    }
    response = self.client.post(reverse('update', kwargs={'pk': nonexistent_id}), data)
    self.assertEqual(response.status_code, 404)
    task = Task.objects.get(pk=self.task.id)
    self.assertEqual(task.task_name, 'Test Task')
    self.assertEqual(task.status_id.status, '未着手')

class TaskDeleteTests(TestCase):
  def setUp(self):
    self.status_not_started = Status.objects.create(status='未着手')
    self.status_completed = Status.objects.create(status='完了')

    self.task = Task.objects.create(
      task_name = 'Test Task',
      status_id = self.status_not_started,
      end_date  = None
    )

  def test_delete_task(self):
    response = self.client.post(reverse('delete', kwargs={'pk': self.task.id}))
    self.assertEqual(response.status_code, 302)
    with self.assertRaises(Task.DoesNotExist):
      Task.objects.get(id=self.task.id)

  def test_delete_task_with_null_id(self):
    null_id = None
    # with self.assertRaises(Task.DoesNotExist):
    #   self.client.post(reverse('delete', kwargs={'pk': null_id}))
